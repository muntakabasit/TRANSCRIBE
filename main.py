from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import whisper
import yt_dlp
import tempfile
import os
import logging
from pydantic import BaseModel
from typing import Optional
from transformers import MT5ForConditionalGeneration, MT5Tokenizer, MarianMTModel, MarianTokenizer
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DAWT-Transcribe v2.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Loading Whisper base model...")
model = whisper.load_model("base")
logger.info("Whisper model loaded successfully")

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

@app.post("/transcribe")
async def transcribe(request: TranscribeRequest):
    if not request.url and not request.file_path:
        raise HTTPException(status_code=400, detail="Provide URL or file_path")
    
    audio_path = None
    is_temp_file = False
    
    try:
        if request.url:
            is_temp_file = True
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(extractor)s-%(id)s.%(ext)s'),
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(request.url, download=True)
                audio_path = ydl.prepare_filename(info)
        else:
            audio_path = request.file_path
        
        if not audio_path or not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            raise HTTPException(status_code=500, detail="Audio file not accessible")
        
        logger.info(f"Transcribing with Whisper: {audio_path}")
        result = model.transcribe(audio_path)
        
        segments = [{"start": seg['start'], "end": seg['end'], "text": seg['text']} for seg in result['segments']]
        full_text = result["text"]
        
        detected_lang = request.lang
        if detected_lang == "en" and lang_models:
            for lang_key, keywords in lang_keywords.items():
                if any(kw.lower() in full_text.lower() for kw in keywords):
                    detected_lang = lang_key
                    logger.info(f"Auto-detected language: {detected_lang}")
                    break
        
        if detected_lang != "en" and lang_models and detected_lang in lang_models:
            try:
                logger.info(f"Enhancing transcription with {detected_lang} MT...")
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
                
                logger.info(f"Translation enhancement complete for {detected_lang}")
            except Exception as e:
                logger.warning(f"Translation failed: {e}. Returning Whisper output only.")
        
        if is_temp_file and audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info(f"Cleaned up temporary file: {audio_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {audio_path}: {e}")
        
        return {
            "full_text": full_text,
            "segments": segments,
            "language": result["language"],
            "detected_mt": detected_lang,
            "duration": result["segments"][-1]["end"] if segments else 0
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transcription error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail="Transcription failed. Please check your audio file or URL.")
    finally:
        if is_temp_file and audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except:
                pass

@app.get("/")
def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
