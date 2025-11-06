from fastapi import FastAPI, HTTPException, Request, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
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
from database import get_db, TranscriptionJob

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

VERSION = "2.1.0"
app = FastAPI(
    title="DAWT-Transcribe",
    version=VERSION,
    description="Sovereign audio transcription with multilingual enhancement"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Loading Whisper tiny model for maximum speed...")
model = whisper.load_model("tiny")
logger.info("Whisper tiny model loaded successfully")

logger.info("Loading multilingual MT models...")
lang_models = {}

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

@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "version": VERSION,
        "whisper_model": "tiny",
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
            "whisper_model": "tiny",
            "mt_models": list(lang_models.keys()) if lang_models else [],
            "supported_platforms": ["TikTok", "Instagram", "YouTube", "Local Files"],
            "output_format": "JSON with timestamped segments"
        },
        "sovereignty": "100% local processing - no cloud APIs"
    })

@app.post("/transcribe")
async def transcribe(request: TranscribeRequest):
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
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(extractor)s-%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
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
        result = model.transcribe(audio_path)
        whisper_time = time.time() - whisper_start
        logger.info(f"[{request_id}] Whisper completed in {whisper_time:.2f}s")
        
        segments = [{"start": seg['start'], "end": seg['end'], "text": seg['text']} for seg in result['segments']]
        full_text = result["text"]
        
        detected_lang = request.lang
        mt_enhanced = False
        
        if detected_lang == "en" and lang_models:
            for lang_key, keywords in lang_keywords.items():
                if any(kw.lower() in full_text.lower() for kw in keywords):
                    detected_lang = lang_key
                    logger.info(f"[{request_id}] Auto-detected language: {detected_lang}")
                    break
        
        if detected_lang != "en" and lang_models and detected_lang in lang_models:
            try:
                logger.info(f"[{request_id}] Enhancing transcription with {detected_lang} MT...")
                mt_start = time.time()
                lm = lang_models[detected_lang]
                texts = [seg["text"] for seg in segments]
                
                inputs = lm["tokenizer"](
                    [f"Translate to English and clarify {detected_lang} pidgin/dialect: {t}" for t in texts],
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
                    if trans_texts[i].strip() and trans_texts[i] != seg["text"]:
                        seg["text_enhanced"] = trans_texts[i]
                        mt_enhanced = True
                
                mt_time = time.time() - mt_start
                logger.info(f"[{request_id}] Translation enhancement complete in {mt_time:.2f}s")
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
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(extractor)s-%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                audio_path = ydl.prepare_filename(info)
            
            # Transcribe
            logger.info(f"[{job_id}] Starting Whisper transcription...")
            result = model.transcribe(audio_path)
            
            segments = [{"start": seg['start'], "end": seg['end'], "text": seg['text']} for seg in result['segments']]
            full_text = result["text"]
            
            # Language detection
            detected_lang = lang
            mt_enhanced = False
            
            if detected_lang == "en" and lang_models:
                for lang_key, keywords in lang_keywords.items():
                    if any(kw.lower() in full_text.lower() for kw in keywords):
                        detected_lang = lang_key
                        break
            
            # MT enhancement (if applicable)
            if detected_lang != "en" and lang_models and detected_lang in lang_models:
                try:
                    lm = lang_models[detected_lang]
                    texts = [seg["text"] for seg in segments]
                    
                    inputs = lm["tokenizer"](
                        [f"Translate to English and clarify {detected_lang} pidgin/dialect: {t}" for t in texts],
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
                        if trans_texts[i].strip() and trans_texts[i] != seg["text"]:
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
            job.error_message = str(e)
            db.commit()
    finally:
        db.close()

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
    
    return JSONResponse({
        "success": True,
        "job_id": job_id,
        "message": "Transcription started! Check status or come back later.",
        "status_url": f"/status/{job_id}",
        "results_url": f"/results/{job_id}"
    })

@app.get("/status/{job_id}")
async def get_status(job_id: str, db: Session = Depends(get_db)):
    """Check if a job is complete"""
    job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JSONResponse({
        "job_id": job_id,
        "status": job.status,
        "created_at": job.created_at.isoformat(),
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "processing_time": job.processing_time
    })

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
    
    return JSONResponse({
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
    })

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

@app.get("/")
def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
