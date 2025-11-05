# DAWT-Transcribe v1

## Overview
DAWT-Transcribe is a sovereign audio transcription API built for processing breath-song clips, Instagram Reels, and vocal samples into timestamped JSON outputs. Uses OpenAI's Whisper model running locally (no cloud dependencies) to maintain data sovereignty. Designed to feed AutoCut's beat analysis and video editing workflows.

## Purpose
- Transcribe audio from URLs (Instagram Reels, YouTube) or uploaded files
- Generate timestamped segments for breath-sync and cut detection
- Provide JSON outputs for AutoCut integration
- Prototype on Replit, then export to Mac Mini for sovereign iPhone Shortcuts workflow

## Current State
- FastAPI backend with `/transcribe` endpoint operational
- Whisper base model for fast local transcription
- yt-dlp integration for Instagram/YouTube audio extraction
- CORS enabled for future React Native mobile bridge
- Test script ready for validation with sample clips

## Recent Changes
- 2025-11-05: Initial blueprint implementation
  - Created FastAPI server with Whisper integration
  - Added yt-dlp for URL-based audio downloads
  - Configured for Replit deployment with port 5000
  - Implemented temporary file handling for secure audio processing

## Project Architecture

### Backend Structure
- `main.py`: FastAPI application with Whisper transcription
- `requirements.txt`: Python dependencies (FastAPI, Whisper, yt-dlp)
- `test.py`: Validation script for testing transcription workflow
- `.gitignore`: Python-specific ignore patterns

### Key Endpoints
- `GET /`: Health check and endpoint listing
- `POST /transcribe`: Main transcription endpoint
  - Accepts: `url` (Instagram/YouTube) or `file_path` (local file)
  - Returns: full transcript, timestamped segments, language, duration

### Dependencies
- **FastAPI** (0.104.1): Web framework
- **Uvicorn** (0.24.0): ASGI server
- **openai-whisper** (20231117): Local Whisper model (sovereign, no API key)
- **yt-dlp** (2024.10.22): Audio download from social platforms
- **python-multipart** (0.0.6): File upload support

### Whisper Model
- Currently using `base` model for speed on Replit free tier
- Can upgrade to `medium` or `large` for improved accuracy on breath-song clips
- Models run entirely local—no external API calls

## User Preferences
- Sovereignty: All processing must remain local (no cloud transcription services)
- Privacy: No data leaks to external services
- Integration focus: Outputs designed for AutoCut beat analysis
- Workflow: Prototype on Replit → Export to Mac Mini → iPhone Shortcuts integration

## Sovereignty Workflow
1. **Replit Phase** (Current): Rapid prototyping and testing
   - Test with Jay-Z clips and breath-song footage
   - Validate JSON output structure for AutoCut
   - Iterate on segment analysis patterns

2. **Local Migration** (Next):
   - Git clone to Mac Mini
   - Run: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - iPhone Shortcuts fetch via local network IP

## Future Enhancements
- `/analyze` endpoint: Pipe segments to librosa for beat detection
- SRT export: Generate subtitle files for video overlays
- Batch processing: Handle multiple clips in single request
- Model upgrade: Switch to Whisper medium/large for vocal pattern accuracy
- AutoCut JSON format: Direct integration with beat-synced editing workflow

## Testing Workflow
1. Upload 30s audio sample via Replit files OR provide Instagram Reel URL
2. Run `python test.py` with URL or use POST request to `/transcribe`
3. Review JSON output: segments, timestamps, language detection
4. Analyze average segment length for breath-sync patterns
5. Export segments to Notes for AutoCut integration

## Notes
- Whisper base model processes ~1-2 mins per clip
- Temporary files auto-cleaned after transcription
- CORS configured for all origins (tighten for production)
- Port 5000 configured for Replit webview compatibility
