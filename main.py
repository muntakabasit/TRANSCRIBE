from fastapi import FastAPI, HTTPException, Request, Depends, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
import whisper
import yt_dlp
import tempfile
import os
import logging
from pydantic import BaseModel, validator
from typing import Optional, Dict, Any, List
from transformers import MT5ForConditionalGeneration, MT5Tokenizer, MarianMTModel, MarianTokenizer
import torch
import time
from datetime import datetime
import json
from sqlalchemy.orm import Session
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
            mt5_tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small")

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
        if v and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError("URL must start with http:// or https://")
        return v

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

def build_ydl_opts(url: str, db: Session) -> dict:
    """Build yt-dlp options with Instagram cookie injection if available"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(tempfile.gettempdir(), '%(extractor)s-%(id)s.%(ext)s'),
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
            logger.info(f"[{request_id}] Downloading audio from URL...")
            is_temp_file = True
            ydl_opts = build_ydl_opts(request.url, db)
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(request.url, download=True)
                    audio_path = ydl.prepare_filename(info)
                logger.info(f"[{request_id}] Audio downloaded successfully")
            except Exception as e:
                logger.error(f"[{request_id}] Download failed: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "download_failed",
                        "message": "Could not download audio from URL. Check URL validity.",
                        "request_id": request_id
                    }
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
        
        detected_lang = request.lang
        mt_enhanced = False
        
        models_dict = get_lang_models()

        if detected_lang == "en" and models_dict:
            for lang_key, keywords in lang_keywords.items():
                if any(kw.lower() in full_text.lower() for kw in keywords):
                    detected_lang = lang_key
                    logger.info(f"[{request_id}] Auto-detected language: {detected_lang}")
                    break

        if detected_lang != "en" and models_dict and detected_lang in models_dict:
            try:
                logger.info(f"[{request_id}] Translating {detected_lang} to English...")
                mt_start = time.time()
                lm = models_dict[detected_lang]
                texts = [seg["text"] for seg in segments]
                
                lang_full_name = {
                    "pidgin": "Pidgin English",
                    "twi": "Twi",
                    "igbo": "Igbo",
                    "yoruba": "Yoruba",
                    "hausa": "Hausa",
                    "swahili": "Swahili",
                    "amharic": "Amharic",
                    "french": "French",
                    "portuguese": "Portuguese",
                    "ewe": "Ewe",
                    "dagbani": "Dagbani"
                }.get(detected_lang, detected_lang.title())
                
                inputs = lm["tokenizer"](
                    [f"translate {lang_full_name} to English: {t}" for t in texts],
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=128
                )
                
                with torch.no_grad():
                    translated = lm["model"].generate(
                        inputs.input_ids,
                        max_length=128,
                        num_beams=4,
                        early_stopping=True
                    )
                
                trans_texts = lm["tokenizer"].batch_decode(translated, skip_special_tokens=True)
                
                for i, seg in enumerate(segments):
                    if trans_texts[i].strip() and len(trans_texts[i]) > 3:
                        seg["text_enhanced"] = trans_texts[i]
                        mt_enhanced = True
                
                mt_time = time.time() - mt_start
                logger.info(f"[{request_id}] Translation complete in {mt_time:.2f}s")
            except Exception as e:
                logger.warning(f"[{request_id}] Translation failed: {e}. Returning Whisper output only.")
        
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
            "detected_mt": detected_lang,
            "mt_enhanced": mt_enhanced,
            "duration": result["segments"][-1]["end"] if segments else 0,
            "segment_count": len(segments),
            "processing_time": round(processing_time, 2),
            "timestamp": datetime.utcnow().isoformat()
        })
    except HTTPException:
        raise
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
        
        job.status = "processing"
        db.commit()
        
        start_time = time.time()
        audio_path = None
        
        try:
            # Download audio
            logger.info(f"[{job_id}] Downloading audio from URL...")
            ydl_opts = build_ydl_opts(url, db)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                audio_path = ydl.prepare_filename(info)
            
            # Check video duration (limit to 21 minutes to prevent crashes)
            video_duration = info.get('duration', 0)
            max_duration = 1260  # 21 minutes (buffer for ~20 min videos)
            if video_duration > max_duration:
                raise ValueError(f"⚠️ Video too long ({video_duration//60} minutes). Maximum: {max_duration//60} minutes. Please use shorter videos to prevent server crashes.")
            
            logger.info(f"[{job_id}] Video duration: {video_duration}s")
            
            # Transcribe
            logger.info(f"[{job_id}] Starting Whisper transcription...")
            whisper_lang = whisper_lang_map.get(lang, "en")
            logger.info(f"[{job_id}] Forcing Whisper language: {whisper_lang} (user selected: {lang})")
            whisper_model = get_whisper_model()
            result = whisper_model.transcribe(audio_path, language=whisper_lang)
            
            segments = [{"start": seg['start'], "end": seg['end'], "text": seg['text']} for seg in result['segments']]
            full_text = result["text"]
            
            # Language detection
            detected_lang = lang
            mt_enhanced = False
            
            models_dict = get_lang_models()

            if detected_lang == "en" and models_dict:
                for lang_key, keywords in lang_keywords.items():
                    if any(kw.lower() in full_text.lower() for kw in keywords):
                        detected_lang = lang_key
                        break

            # MT enhancement (if applicable)
            if detected_lang != "en" and models_dict and detected_lang in models_dict:
                try:
                    lm = models_dict[detected_lang]
                    texts = [seg["text"] for seg in segments]
                    
                    lang_full_name = {
                        "pidgin": "Pidgin English",
                        "twi": "Twi",
                        "igbo": "Igbo",
                        "yoruba": "Yoruba",
                        "hausa": "Hausa",
                        "swahili": "Swahili",
                        "amharic": "Amharic",
                        "french": "French",
                        "portuguese": "Portuguese",
                        "ewe": "Ewe",
                        "dagbani": "Dagbani"
                    }.get(detected_lang, detected_lang.title())
                    
                    inputs = lm["tokenizer"](
                        [f"translate {lang_full_name} to English: {t}" for t in texts],
                        return_tensors="pt",
                        padding=True,
                        truncation=True,
                        max_length=128
                    )
                    
                    with torch.no_grad():
                        translated = lm["model"].generate(
                            inputs.input_ids,
                            max_length=128,
                            num_beams=4,
                            early_stopping=True
                        )
                    
                    trans_texts = lm["tokenizer"].batch_decode(translated, skip_special_tokens=True)
                    
                    for i, seg in enumerate(segments):
                        if trans_texts[i].strip() and len(trans_texts[i]) > 3:
                            seg["text_enhanced"] = trans_texts[i]
                            mt_enhanced = True
                except Exception as e:
                    logger.warning(f"[{job_id}] Translation failed: {e}")
            
            # Cleanup
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            
            processing_time = time.time() - start_time
            
            # Update job with results
            job.status = "completed"
            job.full_text = full_text
            job.segments = json.dumps(segments)
            job.detected_language = result["language"]
            job.detected_mt = detected_lang
            job.mt_enhanced = mt_enhanced
            job.duration = result["segments"][-1]["end"] if segments else 0
            job.segment_count = len(segments)
            job.processing_time = round(processing_time, 2)
            job.completed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"[{job_id}] ✅ Background transcription complete in {processing_time:.2f}s")
            
        except Exception as e:
            logger.error(f"[{job_id}] ❌ Background transcription failed: {str(e)}")
            job.status = "failed"
            
            # Make error messages user-friendly
            error_str = str(e)
            if "not be comfortable for some audiences" in error_str or "Log in for access" in error_str:
                job.error_message = "⚠️ TikTok Age Restriction: This video requires login to download (age-restricted or sensitive content). Please try a different public TikTok video."
            elif "Private video" in error_str or "This video is private" in error_str:
                job.error_message = "⚠️ Private Video: This video is not publicly accessible. Please use a public video URL."
            elif "rate-limit reached" in error_str or "login required" in error_str:
                if "Instagram" in error_str:
                    job.error_message = "⚠️ Instagram Block: Instagram is temporarily blocking downloads. This happens when too many requests are made. Please try: (1) A different Instagram Reel, (2) A TikTok or YouTube URL instead, or (3) Wait 10-15 minutes and try again."
                else:
                    job.error_message = "⚠️ Rate Limited: Too many requests to this platform. Please wait a few minutes and try again, or use a different video URL."
            elif "No video formats found" in error_str:
                job.error_message = "⚠️ Download Failed: This video is blocked or unavailable. Try a different public TikTok, Instagram Reel, or YouTube URL."
            else:
                job.error_message = f"Error: {error_str}"
            
            db.commit()
    finally:
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

        # Transcribe using Whisper
        logger.info(f"🎙️ Starting transcription with language: {lang}")
        whisper_model = get_whisper_model()
        result = whisper_model.transcribe(temp_audio_path, language=lang)

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

        logger.info(f"✅ Transcription complete: {len(segments)} segments")

        response_data = {
            "success": True,
            "full_text": full_text,
            "segments": segments,
            "language": detected_language.upper(),
            "duration": duration
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
    
    # Create job record
    job = TranscriptionJob(
        id=job_id,
        url=request.url,
        language=request.lang,
        status="pending"
    )
    db.add(job)
    db.commit()
    
    # Start background task
    background_tasks.add_task(process_transcription_background, job_id, request.url, request.lang)
    
    logger.info(f"[{job_id}] Job submitted for background processing")
    
    return JSONResponse(add_metadata({
        "success": True,
        "job_id": job_id,
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
        "status": job.status,
        "created_at": job.created_at.isoformat(),
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
        raise HTTPException(status_code=500, detail={"error": "transcription_failed", "message": job.error_message})
    
    if job.status != "completed":
        return JSONResponse({
            "job_id": job_id,
            "status": job.status,
            "message": "Transcription still in progress. Check back soon!"
        })
    
    return JSONResponse(add_metadata({
        "success": True,
        "job_id": job_id,
        "url": job.url,
        "full_text": job.full_text,
        "segments": json.loads(job.segments) if job.segments else [],
        "language": job.detected_language,
        "detected_mt": job.detected_mt,
        "mt_enhanced": job.mt_enhanced,
        "duration": job.duration,
        "segment_count": job.segment_count,
        "processing_time": job.processing_time,
        "created_at": job.created_at.isoformat(),
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
                "url": job.url,
                "status": job.status,
                "language": job.detected_mt or job.language,
                "duration": job.duration,
                "segment_count": job.segment_count,
                "created_at": job.created_at.isoformat(),
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
