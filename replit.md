# DAWT-Transcribe v2.0

## Overview
DAWT-Transcribe v2.0 is a sovereign audio transcription API with multilingual enhancement built for processing Ghanaian Pidgin, breath-song clips, Instagram Reels, TikTok videos, and vocal samples into timestamped JSON outputs. Uses OpenAI's Whisper model + mT5 machine translation running locally (no cloud dependencies) to maintain data sovereignty. Features a Virgil Abloh/Off-White inspired UI with bold typography, quotation marks, and minimalist black-and-white industrial design. Designed to feed AutoCut's beat analysis and video editing workflows.

## Purpose
- Transcribe audio from URLs (TikTok, Instagram Reels, YouTube) or uploaded files
- Enhance transcriptions with AI translation for African languages and dialects
- Generate timestamped segments for breath-sync and cut detection
- Provide JSON outputs for AutoCut integration
- Prototype on Replit, then export to Mac Mini for sovereign iPhone Shortcuts workflow

## Current State (v2.0)
- FastAPI backend with `/transcribe` endpoint operational
- Whisper base model for fast local transcription
- **NEW:** mT5-small multilingual translation models for 11 languages
- **NEW:** Auto-detect Pidgin, Twi, Igbo, Yoruba, Hausa, Swahili, Amharic, French, Portuguese, Ewe, Dagbani
- **NEW:** Virgil Abloh/Off-White inspired frontend UI
- yt-dlp integration for TikTok/Instagram/YouTube audio extraction
- CORS enabled for future React Native mobile bridge
- Graceful fallback when MT models unavailable

## Recent Changes
- **2025-11-05 v2.0:** Multilingual upgrade + Virgil Abloh design
  - Added mT5-small MT models for 11 African/European languages
  - Implemented keyword-based language detection
  - Created Virgil Abloh-inspired UI (quotation marks, industrial labels, B&W aesthetic)
  - Added language selector dropdown with 12 options
  - Enhanced segment display with translation arrows
  - Architect-reviewed multilingual pipeline (PASS)
  
- **2025-11-05 v1.0:** Initial blueprint implementation
  - Created FastAPI server with Whisper integration
  - Added yt-dlp for URL-based audio downloads
  - Configured for Replit deployment with port 5000
  - Implemented temporary file handling for secure audio processing

## Project Architecture

### Backend Structure
- `main.py`: FastAPI application with Whisper + mT5 multilingual pipeline
- `static/index.html`: Virgil Abloh-inspired frontend interface
- `requirements.txt`: Python dependencies (FastAPI, Whisper, yt-dlp, transformers, torch)
- `test.py`: Validation script for testing transcription workflow
- `.gitignore`: Python-specific ignore patterns

### Key Endpoints
- `GET /`: Virgil Abloh UI interface
- `POST /transcribe`: Main transcription endpoint
  - Accepts: `url` (TikTok/Instagram/YouTube), `file_path` (local file), `lang` (language code)
  - Returns: full transcript, timestamped segments, language, detected_mt, duration, text_enhanced (when MT succeeds)

### Supported Languages (v2.0)
1. **English** (auto-detect, default)
2. **Pidgin** (GH/NG) - Ghanaian/Nigerian Pidgin English
3. **Twi** - Ghanaian language
4. **Igbo** - Nigerian language
5. **Yoruba** - Nigerian language
6. **Hausa** - West African language
7. **Swahili** - East African language
8. **Amharic** - Ethiopian language
9. **French** - West/Central African
10. **Portuguese** - African Portuguese
11. **Ewe** - Ghanaian/Togolese language
12. **Dagbani** - Northern Ghanaian language

### Dependencies
- **FastAPI** (0.104.1): Web framework
- **Uvicorn** (0.24.0): ASGI server
- **openai-whisper** (20231117): Local Whisper model (sovereign, no API key)
- **yt-dlp** (2024.10.22): Audio download from social platforms
- **python-multipart** (0.0.6): File upload support
- **transformers** (4.57.1): Hugging Face transformers for MT models
- **torch** (2.3.1): PyTorch for ML models (upgrade to ≥2.6 for Mac deployment)
- **sentencepiece** (0.2.1): Tokenizer for mT5
- **datasets**, **evaluate**, **sacrebleu**, **accelerate**: ML utilities

### Whisper Model
- Currently using `base` model for speed on Replit
- Can upgrade to `medium` or `large` for improved accuracy on breath-song clips
- Models run entirely local—no external API calls

### MT Pipeline (v2.0)
- **Model:** mT5-small (1.2GB) shared across all languages
- **Strategy:** Keyword detection + explicit language selection
- **Keywords:** Each language has 4-5 detection keywords (e.g., "abeg", "wetin" for Pidgin)
- **Enhancement:** Whisper transcript → mT5 translation → `text_enhanced` field added to segments
- **Fallback:** If MT fails, returns Whisper-only output (no errors)
- **Mac Deployment:** Requires torch ≥2.6 for full safetensors support

### Frontend Design (Virgil Abloh / Off-White Aesthetic)
- **Typography:** Bold Helvetica Neue, uppercase labels, tight letter-spacing
- **Quotation Marks:** Decorative quotes around "TRANSCRIBE" heading
- **Industrial Labels:** "AUDIO INPUT" cutout labels on bordered boxes
- **Color Scheme:** Minimal black-on-white with 4px black top stripe
- **Buttons:** Black background with arrow (→) indicator
- **Segments:** Left-border emphasis, enhanced translations with arrow separator
- **Spinners:** Square (no curves) for loading states

## User Preferences
- **Sovereignty:** All processing must remain local (no cloud transcription services)
- **Privacy:** No data leaks to external services
- **Design:** Virgil Abloh/Off-White aesthetic - quotation marks, bold typography, black/white minimalism, industrial styling
- **Integration focus:** Outputs designed for AutoCut beat analysis
- **Workflow:** Prototype on Replit → Export to Mac Mini → iPhone Shortcuts integration
- **Future project queued:** UI/UX design scraper tool (after DAWT-Transcribe complete)

## Sovereignty Workflow
1. **Replit Phase** (Current): Rapid prototyping and testing
   - Test with Ghanaian Pidgin clips and breath-song footage
   - Validate JSON output structure for AutoCut
   - Iterate on segment analysis patterns
   - Test multilingual enhancement with mT5

2. **Local Migration** (Next):
   - Git clone to Mac Mini
   - Run: `pip install -r requirements.txt` (ensure torch ≥2.6)
   - Start: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - iPhone Shortcuts fetch via local network IP
   - Full MT pipeline with safetensors support

## Future Enhancements
- `/analyze` endpoint: Pipe segments to librosa for beat detection
- SRT export: Generate subtitle files for video overlays
- Batch processing: Handle multiple clips in single request
- Model upgrade: Switch to Whisper medium/large for vocal pattern accuracy
- Fine-tuned mT5 models: Train on Pidgin/Twi datasets for better accuracy
- AutoCut JSON format: Direct integration with beat-synced editing workflow
- MarianMT models: Higher-fidelity translations for specific language pairs

## Testing Workflow (v2.0)
1. Open web interface (Virgil Abloh UI)
2. Paste TikTok/Instagram/YouTube URL
3. Select language (or leave as "English (Auto-detect)")
4. Click **PROCESS** → button
5. Review results:
   - Full transcript with detected language
   - Timestamped segments (enhanced translations shown with → arrow)
   - Duration, language code, segment count
6. Export JSON segments to Notes for AutoCut integration

## Notes
- Whisper base model processes ~1-2 mins per clip
- mT5 MT adds ~30-60s for enhancement (only when language detected)
- Temporary files auto-cleaned after transcription
- CORS configured for all origins (tighten for production)
- Port 5000 configured for Replit webview compatibility
- Torch ≥2.6 required for Mac deployment to avoid safetensors warnings
- Design inspired by Virgil Abloh's Off-White aesthetic - user loves the final implementation
