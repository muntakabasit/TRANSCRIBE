from fastapi import FastAPI, HTTPException, Request, Depends, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
import whisper
import yt_dlp
import tempfile
import os
import re
import uuid
import logging
import shutil
import errno
import requests
from pydantic import BaseModel, validator
from typing import Optional, Dict, Any, List
# MT5Tokenizer was removed in transformers 5.x — use AutoTokenizer as the drop-in replacement.
from transformers import MT5ForConditionalGeneration, AutoTokenizer, MarianMTModel, MarianTokenizer
import torch
import time
from datetime import datetime
import json
from sqlalchemy.orm import Session
from urllib.parse import urlparse
from database import get_db, TranscriptionJob, InstagramCookie
import pandas as pd
import io
from crypto_utils import encrypt_cookie, decrypt_cookie
from pydub import AudioSegment

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

VERSION = "2.3.0"
COMPATIBLE_SINCE = "2.0.0"
FORMAT_VERSION = "dawt-transcript-v1"

# ── Disk-space preflight ─────────────────────────────────────────────────────
# Minimum free bytes required before attempting any download.
# At 99% full (1.9 Gi available), even a 50 MB download can tip the disk.
MIN_FREE_BYTES = 400 * 1024 * 1024  # 400 MB hard floor

def check_disk_space(path: str | None = None) -> tuple[bool, int]:
    """Return (has_enough_space, free_bytes) for the temp filesystem."""
    check_path = path or tempfile.gettempdir()
    try:
        usage = shutil.disk_usage(check_path)
        return usage.free >= MIN_FREE_BYTES, usage.free
    except Exception:
        return True, -1  # fail-open — don't block if stat fails

def cleanup_stale_parts(temp_dir: str | None = None, older_than_minutes: int = 30) -> int:
    """
    Remove yt_dlp partial-download (.part) files older than ``older_than_minutes``.
    Only touches files in the system temp directory — never touches project files.
    Returns the count of files removed.
    """
    target = temp_dir or tempfile.gettempdir()
    cutoff = time.time() - (older_than_minutes * 60)
    cleaned = 0
    try:
        for fname in os.listdir(target):
            if fname.endswith('.part'):
                fpath = os.path.join(target, fname)
                try:
                    if os.path.isfile(fpath) and os.path.getmtime(fpath) < cutoff:
                        os.remove(fpath)
                        cleaned += 1
                        logger.debug(f"Removed stale partial download: {fname}")
                except Exception:
                    pass  # best-effort — don't crash cleanup
    except Exception:
        pass
    if cleaned:
        logger.info(f"Temp hygiene: removed {cleaned} stale .part file(s) from {target}")
    return cleaned

app = FastAPI(
    title="DAWT-Transcribe",
    version=VERSION,
    description="Sovereign audio transcription with multilingual enhancement"
)

def add_metadata(data: dict) -> dict:
    """Add version metadata to JSON responses (Excel DNA principle: backward compatibility)"""
    return {
        "meta": {
            "version": VERSION,
            "format": FORMAT_VERSION,
            "compatible_since": COMPATIBLE_SINCE,
            "generated": datetime.utcnow().isoformat() + "Z"
        },
        **data
    }

# Mount static directory only if it exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use lazy loading for models to speed up startup
model = None
lang_models = {}
mt5_model = None
mt5_tokenizer = None

def get_whisper_model():
    """Lazy load Whisper model on first use"""
    global model
    if model is None:
        logger.info("Loading Whisper base model for better accent recognition...")
        model = whisper.load_model("base")
        logger.info("Whisper base model loaded successfully")
    return model

def get_lang_models():
    """Lazy load MT5 models on first use"""
    global lang_models, mt5_model, mt5_tokenizer
    if not lang_models:
        try:
            logger.info("Loading mT5-small for African languages...")
            mt5_model = MT5ForConditionalGeneration.from_pretrained("google/mt5-small")
            mt5_tokenizer = AutoTokenizer.from_pretrained("google/mt5-small")

            lang_models = {
                "pidgin": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "pcm"},
                "twi": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "tw"},
                "igbo": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "ig"},
                "yoruba": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "yo"},
                "hausa": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "ha"},
                "swahili": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "sw"},
                "amharic": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "am"},
                "french": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "fr"},
                "portuguese": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "pt"},
                "ewe": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "ee"},
                "dagbani": {"model": mt5_model, "tokenizer": mt5_tokenizer, "lang_code": "dag"},
            }
            logger.info(f"MT models loaded for {len(lang_models)} languages")
        except Exception as e:
            logger.warning(f"Failed to load MT models: {e}. Translation features will be limited.")
            lang_models = {}
    return lang_models

@app.on_event("startup")
async def startup_event():
    """Log versions, disk state, and readiness at startup."""
    import sys
    logger.info(f"DAWT-Transcribe v{VERSION} is starting up...")
    logger.info(f"Runtime: Python {sys.version.split()[0]} | yt_dlp {yt_dlp.version.__version__}")
    ok, free = check_disk_space()
    free_mb = free // (1024 * 1024) if free >= 0 else -1
    if ok:
        logger.info(f"Disk preflight: {free_mb} MB free — OK")
    else:
        logger.warning(f"⚠️  Disk preflight: only {free_mb} MB free — below {MIN_FREE_BYTES // (1024*1024)} MB floor. URL transcription may fail.")
    stale = cleanup_stale_parts()
    if stale:
        logger.info(f"Startup cleanup: removed {stale} stale partial download(s)")
    logger.info("Models will be loaded on first use (lazy loading)")
    logger.info("Ready to accept requests on 0.0.0.0:8080")

# Health check endpoint for Fly.io
@app.get("/health")
async def health_check():
    """Health check endpoint that responds quickly without loading models"""
    return {
        "status": "healthy",
        "version": VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "DAWT-Transcribe",
        "version": VERSION,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "transcribe": "/transcribe",
            "jobs": "/jobs"
        }
    }

lang_keywords = {
    "pidgin": ["abeg", "wetin", "dey", "na", "fit"],
    "twi": ["medaase", "ɛyɛ", "yɛ", "wo", "me"],
    "igbo": ["biko", "kedu", "nwanne", "nnọọ"],
    "yoruba": ["ẹ ṣeun", "jọwọ", "bawo", "ẹ ku"],
    "hausa": ["sannu", "ina", "ka", "kana"],
    "swahili": ["asante", "pumua", "habari", "ndiyo"],
    "amharic": ["ሰላም", "አመሰግናለሁ", "እንዴት", "ነህ"],
    "french": ["merci", "respire", "bonjour", "comment"],
    "portuguese": ["obrigado", "sinta", "olá", "como"],
    "ewe": ["mede akpe", "yɔ", "afɔ", "wò"],
    "dagbani": ["a yili", "zahir", "naa", "ti"]
}

whisper_lang_map = {
    "en": "en",
    "pidgin": "en",
    "twi": "ak",
    "igbo": "ig",
    "yoruba": "yo",
    "hausa": "ha",
    "swahili": "sw",
    "amharic": "am",
    "french": "fr",
    "portuguese": "pt",
    "ewe": "ee",
    "dagbani": "en"
}

# ── Transcript Cleaning ──────────────────────────────────────────────────────

def clean_transcript(full_text: str, language: str = "en") -> Optional[str]:
    """
    Surface-level readability cleanup for raw Whisper output.

    Allowed: filler-sound removal, word-stutter/repetition removal,
             punctuation normalisation, sentence capitalisation,
             whitespace normalisation.

    Forbidden: paraphrasing, summarising, adding content, grammar rewriting.

    Returns None when:
    - Input is too short to benefit (< 30 words)
    - Cleaning produces no meaningful change (output equals input)
    - Output is empty after cleaning
    - Output has lost more than 35% of original character length (collapse guard)
    - Any exception occurs during cleaning
    """
    try:
        if not full_text:
            return None

        text = full_text.strip()

        # Minimum length gate — very short transcripts don't benefit
        if len(text.split()) < 30:
            return None

        # ── 1. Whitespace normalisation ──────────────────────────────────
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # ── 2. Stutter / word-repetition removal ─────────────────────────
        # Catches "the the", "I I I", "and and" etc.
        text = re.sub(r'\b(\w+)(\s+\1\b)+', r'\1', text, flags=re.IGNORECASE)

        # ── 3. Filler sound removal ───────────────────────────────────────
        # Only unambiguous vocal fillers — no discourse-marker words
        filler_pattern = r'\b(uh+h?|um+|uhh+|umm+|uh-huh|mhm|hmm+)\b,?\s*'
        text = re.sub(filler_pattern, ' ', text, flags=re.IGNORECASE)

        # ── 4. Artifact cleanup after removals ───────────────────────────
        text = re.sub(r'[ \t]{2,}', ' ', text)    # collapse double spaces
        text = re.sub(r'\s+([,.])', r'\1', text)   # remove space before punctuation
        text = re.sub(r',\s*,', ',', text)          # remove duplicate commas

        # ── 5. Sentence capitalisation ───────────────────────────────────
        def _cap_after(m: re.Match) -> str:
            return m.group(0)[:-1] + m.group(0)[-1].upper()
        text = re.sub(r'[.!?]\s+[a-z]', _cap_after, text)

        # ── 6. Capitalise first character ────────────────────────────────
        if text:
            text = text[0].upper() + text[1:]

        # ── 7. Final strip ───────────────────────────────────────────────
        text = text.strip()

        if not text:
            return None

        # Identity check — if nothing changed, don't return a copy as if cleaning helped
        if text == full_text.strip():
            return None

        # Collapse guard — if output is less than 65% of original character length,
        # content may have been incorrectly removed; omit rather than mislead
        if len(text) < len(full_text.strip()) * 0.65:
            logger.warning("clean_transcript: output collapsed below 65% of input — omitting")
            return None

        return text

    except Exception as e:
        logger.warning(f"clean_transcript: failed with {type(e).__name__}: {e}")
        return None

# ─────────────────────────────────────────────────────────────────────────────

class TranscribeRequest(BaseModel):
    url: Optional[str] = None
    file_path: Optional[str] = None
    lang: str = "en"
    
    @validator('lang')
    def validate_lang(cls, v):
        valid_langs = ["en", "pidgin", "twi", "igbo", "yoruba", "hausa", 
                       "swahili", "amharic", "french", "portuguese", "ewe", "dagbani"]
        if v not in valid_langs:
            raise ValueError(f"Invalid language. Must be one of: {', '.join(valid_langs)}")
        return v
    
    @validator('url')
    def validate_url(cls, v):
        return v.strip() if isinstance(v, str) else v

class InstagramCookieRequest(BaseModel):
    session_id: str
    notes: Optional[str] = None

def get_active_instagram_cookie(db: Session) -> Optional[str]:
    """Get the most recent active Instagram cookie"""
    cookie = db.query(InstagramCookie).filter(
        InstagramCookie.is_active == True
    ).order_by(InstagramCookie.created_at.desc()).first()
    
    if cookie:
        cookie.last_used = datetime.utcnow()
        db.commit()
        return decrypt_cookie(cookie.session_id)
    return None

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
_YDL_CACHE_DIR = os.path.join(_REPO_ROOT, ".cache", "yt-dlp")
os.makedirs(_YDL_CACHE_DIR, exist_ok=True)

def build_ydl_opts(url: str, db: Session) -> dict:
    """Build yt-dlp options with Instagram cookie injection if available"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(tempfile.gettempdir(), '%(extractor)s-%(id)s.%(ext)s'),
        # Pin cache to the project-owned .cache dir.
        # ~/.cache is root-owned on this Mac mini, which prevents yt_dlp from
        # writing its nsig/player cache and causes spurious PermissionError warnings.
        'cachedir': _YDL_CACHE_DIR,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'retries': 10,
        'fragment_retries': 10,
        'skip_unavailable_fragments': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
        'extractor_args': {
            'instagram': {
                'api_type': 'graphql'
            }
        }
    }
    
    if 'instagram.com' in url:
        cookie = get_active_instagram_cookie(db)
        if cookie:
            logger.info("🔐 Using Instagram cookie for authenticated download")
            ydl_opts['cookiefile'] = None
            ydl_opts['http_headers']['Cookie'] = f'sessionid={cookie}'
        else:
            logger.warning("⚠️ No Instagram cookie configured - download may fail due to rate limits")
    
    return ydl_opts

@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "version": VERSION,
        "whisper_model": "base",
        "mt_available": len(lang_models) > 0,
        "supported_languages": len(lang_models) + 1,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.get("/api/info")
async def api_info():
    return JSONResponse({
        "name": "DAWT-Transcribe",
        "version": VERSION,
        "description": "Sovereign audio transcription with multilingual enhancement",
        "features": {
            "whisper_model": "base",
            "mt_models": list(lang_models.keys()) if lang_models else [],
            "supported_platforms": ["TikTok", "Instagram", "YouTube", "Local Files"],
            "output_format": "JSON with timestamped segments"
        },
        "sovereignty": "100% local processing - no cloud APIs"
    })

@app.post("/instagram/cookie")
async def add_instagram_cookie(request: InstagramCookieRequest, db: Session = Depends(get_db)):
    """Add Instagram session cookie for reliable downloads"""
    try:
        encrypted_session = encrypt_cookie(request.session_id)
        
        db.query(InstagramCookie).update({"is_active": False})
        db.commit()
        
        new_cookie = InstagramCookie(
            session_id=encrypted_session,
            notes=request.notes,
            is_active=True
        )
        db.add(new_cookie)
        db.commit()
        
        logger.info("Instagram cookie added successfully")
        return JSONResponse({
            "success": True,
            "message": "Instagram cookie added! Instagram downloads should now work reliably.",
            "expires_info": "Instagram cookies typically last 30-90 days. Update when you see failures."
        })
    except Exception as e:
        logger.error(f"Failed to add Instagram cookie: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/instagram/cookie/status")
async def get_cookie_status(db: Session = Depends(get_db)):
    """Check if Instagram cookie is configured"""
    cookie = db.query(InstagramCookie).filter(
        InstagramCookie.is_active == True
    ).order_by(InstagramCookie.created_at.desc()).first()
    
    if cookie:
        return JSONResponse({
            "configured": True,
            "created_at": cookie.created_at.isoformat(),
            "last_used": cookie.last_used.isoformat() if cookie.last_used else None,
            "notes": cookie.notes
        })
    else:
        return JSONResponse({
            "configured": False,
            "message": "No Instagram cookie configured. Add one to enable reliable Instagram downloads."
        })

@app.delete("/instagram/cookie")
async def delete_instagram_cookie(db: Session = Depends(get_db)):
    """Delete/deactivate Instagram cookie"""
    db.query(InstagramCookie).update({"is_active": False})
    db.commit()
    logger.info("Instagram cookie deactivated")
    return JSONResponse({
        "success": True,
        "message": "Instagram cookie removed. Instagram downloads will use anonymous mode (may fail)."
    })

# ---------------------------------------------------------------------------
# Instagram fallback downloaders
# ---------------------------------------------------------------------------

def try_cobalt_download(url: str) -> Optional[str]:
    """Layer 1 fallback: cobalt.tools API"""
    try:
        resp = requests.post(
            "https://api.cobalt.tools/",
            json={"url": url},
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            timeout=30
        )
        if resp.status_code != 200:
            logger.warning(f"cobalt.tools returned {resp.status_code}")
            return None

        data = resp.json()
        if data.get("status") not in ("tunnel", "redirect", "stream"):
            logger.warning(f"cobalt.tools unexpected status: {data.get('status')}")
            return None

        media_url = data.get("url")
        if not media_url:
            return None

        media_resp = requests.get(media_url, timeout=120, stream=True)
        if media_resp.status_code != 200:
            return None

        temp_path = os.path.join(tempfile.gettempdir(), f"cobalt_{uuid.uuid4().hex}.mp4")
        with open(temp_path, "wb") as f:
            for chunk in media_resp.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"cobalt.tools download succeeded: {temp_path}")
        return temp_path
    except Exception as e:
        logger.warning(f"cobalt.tools failed: {e}")
        return None


def try_embed_download(url: str) -> Optional[str]:
    """Layer 2 fallback: Instagram embed scrape"""
    try:
        match = re.search(r'instagram\.com/(?:reel|p|tv)/([A-Za-z0-9_-]+)', url)
        if not match:
            return None

        post_id = match.group(1)
        embed_url = f"https://www.instagram.com/p/{post_id}/embed/"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }

        resp = requests.get(embed_url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return None

        # Try several patterns Instagram has used over time
        video_match = (
            re.search(r'"video_url":"([^"]+)"', resp.text) or
            re.search(r'"contentUrl":"([^"]+)"', resp.text) or
            re.search(r'<source src="([^"]+)"', resp.text)
        )
        if not video_match:
            logger.warning("Embed method: no video URL found in embed HTML")
            return None

        video_url = video_match.group(1).replace("\\/", "/")
        media_resp = requests.get(video_url, headers=headers, timeout=60, stream=True)
        if media_resp.status_code != 200:
            return None

        temp_path = os.path.join(tempfile.gettempdir(), f"embed_{uuid.uuid4().hex}.mp4")
        with open(temp_path, "wb") as f:
            for chunk in media_resp.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"Embed method download succeeded: {temp_path}")
        return temp_path
    except Exception as e:
        logger.warning(f"Embed method failed: {e}")
        return None


def instagram_friendly_error(error_str: str) -> str:
    """Return a user-friendly message for Instagram download failures."""
    if "not be comfortable" in error_str or "Log in for access" in error_str:
        return "This Reel requires a login (age-restricted). Try a different public video."
    if "Private video" in error_str or "This video is private" in error_str:
        return "This video is private. Please use a public Instagram Reel."
    return (
        "Instagram blocked this download. "
        "Try a different public Reel, wait a few minutes, or use a YouTube/TikTok link instead."
    )


def normalize_url(url: str) -> Optional[str]:
    if not url:
        return None
    normalized = url.strip()
    return normalized or None


def is_valid_url(url: Optional[str]) -> bool:
    if not url:
        return False
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def guess_platform(url: Optional[str]) -> str:
    if not url:
        return "unknown"

    host = urlparse(url).netloc.lower()
    if "instagram.com" in host:
        return "instagram"
    if "tiktok.com" in host:
        return "tiktok"
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    return "unknown"


def set_job_state(job: TranscriptionJob, db: Session, state: str, **extra_fields):
    job.state = state
    job.status = state
    job.updated_at = datetime.utcnow()
    for key, value in extra_fields.items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)


def fail_job(job: TranscriptionJob, db: Session, failure_code: str, failure_message: str):
    now = datetime.utcnow()
    job.state = "failed"
    job.status = "failed"
    job.failure_code = failure_code
    job.failure_message = failure_message
    job.error_message = failure_message
    job.updated_at = now
    job.completed_at = now
    db.commit()
    db.refresh(job)


def complete_job(job: TranscriptionJob, db: Session):
    now = datetime.utcnow()
    job.state = "completed"
    job.status = "completed"
    job.failure_code = None
    job.failure_message = None
    job.error_message = None
    job.transcription_id = job.id
    job.updated_at = now
    job.completed_at = now
    db.commit()
    db.refresh(job)


def probe_failure_message(platform: str) -> str:
    if platform == "instagram":
        return "Could not inspect this Instagram URL. The Reel may be unavailable, private, or blocked."
    if platform == "tiktok":
        return "Could not inspect this TikTok URL. The video may be unavailable, private, or blocked."
    if platform == "youtube":
        return "Could not inspect this YouTube URL. The video may be unavailable, private, or blocked."
    return "Could not inspect this URL. Check that the link is public and try again."


def classify_download_error(url: str, error_str: str) -> tuple[str, str]:
    """
    Map a yt_dlp / download exception string to a stable (error_code, user_message) pair.

    error_codes  →  what actually happened (machine-readable, for logs/DB):
        disk_full       — ENOSPC / no space left on device
        extractor_error — yt_dlp couldn't extract; platform or extractor issue
        no_audio        — page found but no usable audio stream
        download_failed — generic network / HTTP failure

    user_message → calm, short text safe to show in the app.
    """
    err_lower = error_str.lower()

    # ── 1. Disk full ─────────────────────────────────────────────────────────
    if "no space left on device" in err_lower or "errno 28" in err_lower or "[errno 28]" in err_lower:
        logger.error(f"ENOSPC during download for {url}: {error_str[:200]}")
        return ("disk_full", "Not enough storage to process this right now. Try again shortly.")

    # ── 2. Unsupported / no extractor ────────────────────────────────────────
    if "unsupported url" in err_lower or "no suitable extractor" in err_lower:
        logger.warning(f"No yt_dlp extractor for URL: {url}")
        return ("extractor_error", "This link isn't supported. Try YouTube, Instagram, or TikTok.")

    # ── 3. No audio stream ───────────────────────────────────────────────────
    if "no video formats found" in err_lower or "no audio" in err_lower or "requested format is not available" in err_lower:
        return ("no_audio", "No audio found in this video. Try a different link.")

    # ── 4. Platform-specific extractor errors ────────────────────────────────
    if "tiktok.com" in url:
        if "login" in err_lower or "http error 403" in err_lower or "private" in err_lower:
            logger.warning(f"TikTok extractor blocked: {error_str[:200]}")
            return ("extractor_error", "TikTok blocked this download. Try a different public TikTok.")
        # Any other TikTok failure is still an extractor issue, not our bug
        logger.warning(f"TikTok extractor failed (upstream): {error_str[:200]}")
        return ("extractor_error", "Could not download this TikTok. The video may be private or restricted.")

    if "instagram.com" in url:
        return ("extractor_error", instagram_friendly_error(error_str))

    # ── 5. Auth / private ────────────────────────────────────────────────────
    if "private video" in err_lower or "this video is private" in err_lower:
        return ("extractor_error", "This video is private. Use a public video URL.")

    if "not be comfortable" in err_lower or "log in for access" in err_lower:
        return ("extractor_error", "This video requires a login. Try a different public video.")

    # ── 6. Generic fallback ──────────────────────────────────────────────────
    return ("download_failed", "Could not download audio from this URL. Check that the link is public and try again.")


def download_failure_message(url: str, error_str: str) -> str:
    """Thin wrapper kept for background-task callers. Delegates to classify_download_error."""
    _, message = classify_download_error(url, error_str)
    return message


@app.post("/transcribe")
async def transcribe(request: TranscribeRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    request_id = f"req_{int(time.time() * 1000)}"
    
    logger.info(f"[{request_id}] New transcription request - lang: {request.lang}")
    
    if not request.url and not request.file_path:
        logger.error(f"[{request_id}] Missing input: no URL or file_path provided")
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "missing_input",
                "message": "Provide either 'url' or 'file_path'",
                "request_id": request_id
            }
        )
    
    audio_path = None
    is_temp_file = False

    try:
        if request.url:
            # ── Disk preflight ────────────────────────────────────────────────
            # Fail before touching the network so we don't leave a partial file.
            has_space, free_bytes = check_disk_space()
            if not has_space:
                free_mb = free_bytes // (1024 * 1024) if free_bytes >= 0 else -1
                logger.error(f"[{request_id}] ENOSPC preflight: {free_mb} MB free — refusing download")
                raise HTTPException(
                    status_code=507,
                    detail={
                        "error": "disk_full",
                        "message": "Not enough storage to process this right now. Try again shortly.",
                        "request_id": request_id
                    }
                )

            # ── Stale-part cleanup before download ────────────────────────────
            cleanup_stale_parts()

            logger.info(f"[{request_id}] Downloading audio from URL...")
            is_temp_file = True
            ydl_opts = build_ydl_opts(request.url, db)
            ydl_error_str = None

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(request.url, download=True)
                    audio_path = ydl.prepare_filename(info)
                logger.info(f"[{request_id}] yt_dlp download succeeded")
            except Exception as e:
                ydl_error_str = str(e)
                # Surface ENOSPC immediately without going through the fallback chain
                if isinstance(e, OSError) and e.errno == errno.ENOSPC:
                    logger.error(f"[{request_id}] ENOSPC during download: {ydl_error_str}")
                    raise HTTPException(
                        status_code=507,
                        detail={
                            "error": "disk_full",
                            "message": "Not enough storage to process this right now. Try again shortly.",
                            "request_id": request_id
                        }
                    )
                error_code_check, _ = classify_download_error(request.url, ydl_error_str)
                logger.warning(f"[{request_id}] yt_dlp failed [{error_code_check}]: {ydl_error_str[:300]}")

            # Fallback chain for Instagram
            if not audio_path and "instagram.com" in request.url:
                logger.info(f"[{request_id}] Trying cobalt.tools fallback...")
                audio_path = try_cobalt_download(request.url)

                if not audio_path:
                    logger.info(f"[{request_id}] Trying embed fallback...")
                    audio_path = try_embed_download(request.url)

            if not audio_path:
                error_code, user_message = classify_download_error(request.url, ydl_error_str or "")
                logger.warning(f"[{request_id}] All download attempts failed [{error_code}]")
                status_code = 507 if error_code == "disk_full" else 400
                raise HTTPException(
                    status_code=status_code,
                    detail={"error": error_code, "message": user_message, "request_id": request_id}
                )
        else:
            audio_path = request.file_path
        
        if not audio_path or not os.path.exists(audio_path):
            logger.error(f"[{request_id}] Audio file not found: {audio_path}")
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "file_not_found",
                    "message": "Audio file not accessible",
                    "request_id": request_id
                }
            )
        
        logger.info(f"[{request_id}] Starting Whisper transcription...")
        whisper_start = time.time()
        
        whisper_lang = whisper_lang_map.get(request.lang, "en")
        logger.info(f"[{request_id}] Forcing Whisper language: {whisper_lang} (user selected: {request.lang})")
        whisper_model = get_whisper_model()
        result = whisper_model.transcribe(audio_path, language=whisper_lang)
        
        whisper_time = time.time() - whisper_start
        logger.info(f"[{request_id}] Whisper completed in {whisper_time:.2f}s")
        
        segments = [{"start": seg['start'], "end": seg['end'], "text": seg['text']} for seg in result['segments']]
        full_text = result["text"]

        # Cleaning pass — best-effort, never blocks success
        cleaned_transcript = clean_transcript(full_text, language=request.lang)
        if cleaned_transcript:
            logger.info(f"[{request_id}] cleaned_transcript produced ({len(cleaned_transcript)} chars)")
        else:
            logger.info(f"[{request_id}] cleaned_transcript omitted")

        if is_temp_file and audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info(f"[{request_id}] Cleaned up temporary file: {audio_path}")
            except Exception as e:
                logger.warning(f"[{request_id}] Failed to cleanup temp file {audio_path}: {e}")

        processing_time = time.time() - start_time
        logger.info(f"[{request_id}] ✅ Transcription complete in {processing_time:.2f}s")

        return JSONResponse({
            "success": True,
            "request_id": request_id,
            "full_text": full_text,
            "segments": segments,
            "language": result["language"],
            "duration": result["segments"][-1]["end"] if segments else 0,
            "segment_count": len(segments),
            "processing_time": round(processing_time, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "cleaned_transcript": cleaned_transcript,
        })
    except HTTPException:
        raise
    except OSError as e:
        # Catch ENOSPC that surfaces during Whisper write / temp operations
        if e.errno == errno.ENOSPC:
            logger.error(f"[{request_id}] ENOSPC during transcription: {e}")
            raise HTTPException(
                status_code=507,
                detail={
                    "error": "disk_full",
                    "message": "Not enough storage to process this right now. Try again shortly.",
                    "request_id": request_id
                }
            )
        logger.error(f"[{request_id}] ❌ OSError: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "transcription_failed",
                "message": "Transcription failed. Please check your audio file or URL.",
                "error_type": type(e).__name__,
                "request_id": request_id
            }
        )
    except Exception as e:
        logger.error(f"[{request_id}] ❌ Transcription error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "transcription_failed",
                "message": "Transcription failed. Please check your audio file or URL.",
                "error_type": type(e).__name__,
                "request_id": request_id
            }
        )
    finally:
        if is_temp_file and audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.debug(f"[{request_id}] Cleanup: removed temp file")
            except Exception as cleanup_err:
                logger.debug(f"[{request_id}] Cleanup warning: {cleanup_err}")

def process_transcription_background(job_id: str, url: str, lang: str):
    """Background task to process transcription"""
    db = SessionLocal()
    try:
        job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
        if not job:
            return

        start_time = time.time()
        audio_path = None
        
        try:
            set_job_state(job, db, "downloading")

            # Download audio
            logger.info(f"[{job_id}] Downloading audio from URL...")
            ydl_opts = build_ydl_opts(url, db)
            info = None
            probe_error_str = None
            ydl_error_str = None

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
            except Exception as probe_err:
                probe_error_str = str(probe_err)
                logger.warning(f"[{job_id}] Probe failed: {probe_error_str}")
                if job.platform_guess != "instagram":
                    fail_job(job, db, "probe_failed", probe_failure_message(job.platform_guess or "unknown"))
                    return

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    audio_path = ydl.prepare_filename(info)
            except Exception as ydl_err:
                ydl_error_str = str(ydl_err)
                logger.warning(f"[{job_id}] yt_dlp failed: {ydl_error_str}")
                if "instagram.com" in url:
                    logger.info(f"[{job_id}] Trying cobalt.tools fallback...")
                    audio_path = try_cobalt_download(url)
                    if not audio_path:
                        logger.info(f"[{job_id}] Trying embed fallback...")
                        audio_path = try_embed_download(url)
                if not audio_path:
                    if probe_error_str:
                        fail_job(job, db, "probe_failed", probe_failure_message(job.platform_guess or "unknown"))
                    else:
                        fail_job(job, db, "download_failed", download_failure_message(url, ydl_error_str))
                    return

            # Check video duration (limit to 21 minutes to prevent crashes)
            video_duration = info.get('duration', 0) if info else 0
            max_duration = 1260  # 21 minutes (buffer for ~20 min videos)
            if video_duration > max_duration:
                fail_job(
                    job,
                    db,
                    "download_failed",
                    f"Video too long ({video_duration//60} minutes). Maximum: {max_duration//60} minutes."
                )
                return
            
            logger.info(f"[{job_id}] Video duration: {video_duration}s")
            
            # Transcribe
            set_job_state(job, db, "transcribing")
            logger.info(f"[{job_id}] Starting Whisper transcription...")
            whisper_lang = whisper_lang_map.get(lang, "en")
            logger.info(f"[{job_id}] Forcing Whisper language: {whisper_lang} (user selected: {lang})")
            whisper_model = get_whisper_model()
            result = whisper_model.transcribe(audio_path, language=whisper_lang)
            
            segments = [{"start": seg['start'], "end": seg['end'], "text": seg['text']} for seg in result['segments']]
            full_text = result["text"]

            # Cleanup
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)

            processing_time = time.time() - start_time

            # Update job with results
            job.full_text = full_text
            job.segments = json.dumps(segments)
            job.detected_language = result["language"]
            job.duration = result["segments"][-1]["end"] if segments else 0
            job.segment_count = len(segments)
            job.processing_time = round(processing_time, 2)
            complete_job(job, db)
            
            logger.info(f"[{job_id}] ✅ Background transcription complete in {processing_time:.2f}s")
            
        except Exception as e:
            logger.error(f"[{job_id}] ❌ Background transcription failed: {str(e)}")
            fail_job(job, db, "transcription_failed", "Transcription failed. Please check your audio source and try again.")
    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception:
                pass
        db.close()

@app.post("/transcribe_file")
async def transcribe_file(
    file: UploadFile = File(...),
    lang: str = Form("en"),
    db: Session = Depends(get_db)
):
    """Transcribe an uploaded audio file"""
    logger.info(f"📁 Received file upload: {file.filename}")

    # Validate language
    valid_langs = ["en", "pidgin", "twi", "igbo", "yoruba", "hausa",
                   "swahili", "amharic", "french", "portuguese", "ewe", "dagbani"]
    if lang not in valid_langs:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid language. Must be one of: {', '.join(valid_langs)}"
        )

    temp_audio_path = None

    try:
        # Save uploaded file to temp location
        temp_dir = tempfile.mkdtemp()
        temp_audio_path = os.path.join(temp_dir, file.filename)

        with open(temp_audio_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"💾 Saved file to: {temp_audio_path}")

        # Get audio duration
        audio = AudioSegment.from_file(temp_audio_path)
        duration = len(audio) / 1000.0  # Convert ms to seconds

        # Transcribe using Whisper with proper language mapping
        logger.info(f"🎙️ Starting transcription with language: {lang}")
        whisper_lang = whisper_lang_map.get(lang, "en")
        logger.info(f"Forcing Whisper language: {whisper_lang} (user selected: {lang})")
        whisper_model = get_whisper_model()
        result = whisper_model.transcribe(temp_audio_path, language=whisper_lang)

        # Format segments
        segments = []
        for segment in result.get("segments", []):
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })

        full_text = result.get("text", "").strip()
        detected_language = result.get("language", lang)

        # Cleaning pass — best-effort, never blocks success
        cleaned_transcript = clean_transcript(full_text, language=lang)
        if cleaned_transcript:
            logger.info(f"✅ Transcription complete: {len(segments)} segments, cleaned_transcript produced")
        else:
            logger.info(f"✅ Transcription complete: {len(segments)} segments, cleaned_transcript omitted")

        response_data = {
            "success": True,
            "full_text": full_text,
            "segments": segments,
            "language": detected_language.upper(),
            "duration": duration,
            "cleaned_transcript": cleaned_transcript,
        }

        return JSONResponse(add_metadata(response_data))

    except Exception as e:
        logger.error(f"❌ Transcription failed: {str(e)}")
        return JSONResponse(
            add_metadata({
                "success": False,
                "error": str(e)
            }),
            status_code=500
        )
    finally:
        # Clean up temp file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
                os.rmdir(os.path.dirname(temp_audio_path))
                logger.info(f"🗑️ Cleaned up temp file")
            except Exception as e:
                logger.warning(f"Failed to clean up temp file: {e}")

@app.post("/submit")
async def submit_job(request: TranscribeRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Submit a transcription job and get job ID immediately"""
    if not request.url:
        raise HTTPException(status_code=400, detail="URL is required for background jobs")
    
    job_id = f"job_{int(time.time() * 1000)}"
    now = datetime.utcnow()
    
    # Create job record
    normalized_url = normalize_url(request.url)
    platform = guess_platform(normalized_url)
    job = TranscriptionJob(
        id=job_id,
        url=normalized_url or request.url,
        original_url=request.url,
        normalized_url=normalized_url,
        platform_guess=platform,
        language=request.lang,
        status="received",
        state="received",
        retry_count=0,
        created_at=now,
        updated_at=now,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    set_job_state(job, db, "validating")

    if not is_valid_url(normalized_url):
        fail_job(job, db, "invalid_url", "URL must start with http:// or https:// and include a valid host.")
        return JSONResponse(
            add_metadata({
                "success": False,
                "job_id": job_id,
                "state": job.state,
                "failure_code": job.failure_code,
                "failure_message": job.failure_message,
            }),
            status_code=400
        )

    if platform == "unknown":
        fail_job(job, db, "unsupported_platform", "Unsupported platform. Use an Instagram, TikTok, or YouTube URL.")
        return JSONResponse(
            add_metadata({
                "success": False,
                "job_id": job_id,
                "state": job.state,
                "failure_code": job.failure_code,
                "failure_message": job.failure_message,
            }),
            status_code=400
        )

    set_job_state(job, db, "accepted", url=normalized_url)
    
    # Start background task
    background_tasks.add_task(process_transcription_background, job_id, normalized_url, request.lang)
    
    logger.info(f"[{job_id}] Job submitted for background processing")
    
    return JSONResponse(add_metadata({
        "success": True,
        "job_id": job_id,
        "state": job.state,
        "original_url": job.original_url,
        "normalized_url": job.normalized_url,
        "platform_guess": job.platform_guess,
        "message": "Transcription started! Check status or come back later.",
        "status_url": f"/status/{job_id}",
        "results_url": f"/results/{job_id}"
    }))

@app.get("/status/{job_id}")
async def get_status(job_id: str, db: Session = Depends(get_db)):
    """Check if a job is complete"""
    job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JSONResponse(add_metadata({
        "job_id": job_id,
        "state": job.state or job.status,
        "status": job.status,
        "original_url": job.original_url or job.url,
        "normalized_url": job.normalized_url,
        "platform_guess": job.platform_guess,
        "failure_code": job.failure_code,
        "failure_message": job.failure_message,
        "transcription_id": job.transcription_id,
        "retry_count": job.retry_count or 0,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "processing_time": job.processing_time
    }))

@app.get("/results/{job_id}")
async def get_results(job_id: str, db: Session = Depends(get_db)):
    """Get full transcription results"""
    job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status == "failed":
        raise HTTPException(
            status_code=500,
            detail={
                "error": job.failure_code or "transcription_failed",
                "message": job.failure_message or job.error_message,
                "job_id": job_id,
                "state": job.state or job.status,
            }
        )
    
    if job.status != "completed":
        return JSONResponse({
            "job_id": job_id,
            "state": job.state or job.status,
            "status": job.status,
            "failure_code": job.failure_code,
            "failure_message": job.failure_message,
            "message": "Transcription still in progress. Check back soon!"
        })
    
    return JSONResponse(add_metadata({
        "success": True,
        "job_id": job_id,
        "url": job.normalized_url or job.url,
        "original_url": job.original_url or job.url,
        "normalized_url": job.normalized_url,
        "platform_guess": job.platform_guess,
        "state": job.state or job.status,
        "failure_code": job.failure_code,
        "failure_message": job.failure_message,
        "transcription_id": job.transcription_id,
        "retry_count": job.retry_count or 0,
        "full_text": job.full_text,
        "segments": json.loads(job.segments) if job.segments else [],
        "language": job.detected_language,
        "detected_mt": job.detected_mt,
        "mt_enhanced": job.mt_enhanced,
        "duration": job.duration,
        "segment_count": job.segment_count,
        "processing_time": job.processing_time,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
        "completed_at": job.completed_at.isoformat(),
        "corrected_text": job.corrected_text,
        "corrected_segments": json.loads(job.corrected_segments) if job.corrected_segments else None,
        "corrected_at": job.corrected_at.isoformat() if job.corrected_at else None
    }))

@app.get("/history")
async def get_history(limit: int = 20, db: Session = Depends(get_db)):
    """Get recent transcription history"""
    jobs = db.query(TranscriptionJob).order_by(TranscriptionJob.created_at.desc()).limit(limit).all()
    
    return JSONResponse({
        "jobs": [
            {
                "job_id": job.id,
                "url": job.normalized_url or job.url,
                "original_url": job.original_url or job.url,
                "platform_guess": job.platform_guess,
                "state": job.state or job.status,
                "status": job.status,
                "failure_code": job.failure_code,
                "language": job.detected_mt or job.language,
                "duration": job.duration,
                "segment_count": job.segment_count,
                "created_at": job.created_at.isoformat(),
                "updated_at": job.updated_at.isoformat() if job.updated_at else None,
                "completed_at": job.completed_at.isoformat() if job.completed_at else None
            }
            for job in jobs
        ]
    })

from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=__import__('database').engine)

@app.post("/correct/{job_id}")
async def save_corrections(job_id: str, request: Request, db: Session = Depends(get_db)):
    """Save user corrections for a transcription"""
    job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    data = await request.json()
    
    job.corrected_text = data.get("corrected_text")
    job.corrected_segments = json.dumps(data.get("corrected_segments")) if data.get("corrected_segments") else None
    job.corrected_at = datetime.utcnow()
    
    db.commit()
    
    logger.info(f"[{job_id}] Corrections saved")
    
    return JSONResponse({
        "success": True,
        "message": "Corrections saved successfully"
    })

@app.get("/export/training")
async def export_training_data(db: Session = Depends(get_db)):
    """Export all corrections as training data pairs"""
    jobs = db.query(TranscriptionJob).filter(
        TranscriptionJob.corrected_text.isnot(None)
    ).all()
    
    training_pairs = []
    for job in jobs:
        if job.corrected_segments:
            original_segments = json.loads(job.segments) if job.segments else []
            corrected_segments = json.loads(job.corrected_segments)
            
            for i, (orig, corr) in enumerate(zip(original_segments, corrected_segments)):
                if orig.get("text") != corr.get("text"):
                    training_pairs.append({
                        "job_id": job.id,
                        "segment_index": i,
                        "original": orig.get("text"),
                        "corrected": corr.get("text"),
                        "language": job.detected_language,
                        "timestamp_start": orig.get("start"),
                        "timestamp_end": orig.get("end")
                    })
    
    return JSONResponse({
        "total_corrections": len(training_pairs),
        "training_pairs": training_pairs
    })

@app.get("/export/{job_id}/csv")
async def export_csv(job_id: str, db: Session = Depends(get_db)):
    """Export transcription as CSV file (Excel-compatible)"""
    job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    segments = json.loads(job.segments) if job.segments else []
    corrected_segments = json.loads(job.corrected_segments) if job.corrected_segments else None
    
    data = []
    for i, segment in enumerate(segments):
        corrected_seg = corrected_segments[i] if corrected_segments and i < len(corrected_segments) else None
        
        text = corrected_seg.get('text', segment.get('text', '')).strip() if corrected_seg else segment.get('text', '').strip()
        translation = segment.get('text_enhanced', '').strip()
        
        data.append({
            "Start Time": f"{segment.get('start', 0):.2f}",
            "End Time": f"{segment.get('end', 0):.2f}",
            "Duration": f"{segment.get('end', 0) - segment.get('start', 0):.2f}",
            "Text": text,
            "MT Enhanced": translation if translation else ''
        })
    
    df = pd.DataFrame(data)
    
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=transcript_{job_id}.csv"}
    )

@app.get("/export/{job_id}/xlsx")
async def export_xlsx(job_id: str, db: Session = Depends(get_db)):
    """Export transcription as Excel file"""
    job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    segments = json.loads(job.segments) if job.segments else []
    corrected_segments = json.loads(job.corrected_segments) if job.corrected_segments else None
    
    data = []
    for i, segment in enumerate(segments):
        corrected_seg = corrected_segments[i] if corrected_segments and i < len(corrected_segments) else None
        
        text = corrected_seg.get('text', segment.get('text', '')).strip() if corrected_seg else segment.get('text', '').strip()
        translation = segment.get('text_enhanced', '').strip()
        
        data.append({
            "Start Time": f"{segment.get('start', 0):.2f}",
            "End Time": f"{segment.get('end', 0):.2f}",
            "Duration": f"{segment.get('end', 0) - segment.get('start', 0):.2f}",
            "Text": text,
            "MT Enhanced": translation if translation else ''
        })
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Transcript')
        
        workbook = writer.book
        worksheet = writer.sheets['Transcript']
        
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=transcript_{job_id}.xlsx"}
    )

# ── Yaro Handoff Mock ────────────────────────────────────────────────────────
# Temporary validation endpoint — remove after Yaro handoff is locked.
# Usage: set YaroClient.endpointURL = "http://192.168.0.90:5001/yaro-mock?scenario=<x>"
# where <x> is one of: accepted | blocked | clarification | malformed

@app.post("/yaro-mock")
async def yaro_mock(request: Request):
    """
    Minimal Yaro intake mock for handoff response-shape validation.
    Reads ?scenario= query param and returns the corresponding response shape.
    """
    scenario = request.query_params.get("scenario", "accepted")

    if scenario == "accepted":
        return JSONResponse({
            "status": "capture_accepted",
            "capture_id": "mock-capture-a1b2c3d4"
        })

    if scenario == "blocked":
        return JSONResponse({
            "status": "capture_blocked",
            "reason": "This capture appears to duplicate an existing Yaro entry."
        })

    if scenario == "clarification":
        return JSONResponse({
            "status": "needs_clarification",
            "clarification_prompt": "What is the primary theme of this capture?"
        })

    if scenario == "malformed":
        # Returns capture_accepted but omits capture_id — tests malformed guard
        return JSONResponse({
            "status": "capture_accepted"
        })

    return JSONResponse(
        {"error": f"Unknown scenario: {scenario}. Use accepted|blocked|clarification|malformed"},
        status_code=400
    )
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/results.html")
def results_page():
    return FileResponse("static/results.html")

@app.get("/history.html")
def history_page():
    return FileResponse("static/history.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
