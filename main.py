from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import whisper
import yt_dlp
import tempfile
import os
import logging
from pydantic import BaseModel
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DAWT-Transcribe v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = whisper.load_model("base")

class TranscribeRequest(BaseModel):
    url: Optional[str] = None
    file_path: Optional[str] = None

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
        
        result = model.transcribe(audio_path)
        
        segments = [{"start": seg['start'], "end": seg['end'], "text": seg['text']} for seg in result['segments']]
        
        return {
            "full_text": result["text"],
            "segments": segments,
            "language": result["language"],
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
                logger.info(f"Cleaned up temporary file: {audio_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {audio_path}: {e}")

@app.get("/")
def root():
    return {"status": "DAWT-Transcribe running", "endpoints": ["/transcribe (POST JSON)"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
