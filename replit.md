# DAWT-Transcribe v2.3

## Overview
DAWT-Transcribe v2.3 is a sovereign audio transcription API designed for processing multilingual audio, including Ghanaian Pidgin, breath-song clips, Instagram Reels, TikTok videos, and vocal samples. It outputs timestamped JSON using local OpenAI Whisper and mT5 machine translation models to ensure data sovereignty. Key features include asynchronous job processing with browser notifications, persistent transcript history, AI-friendly export formats (Markdown, JSON, ChatGPT-ready), and transcription editing for fine-tuning datasets. The UI is inspired by Virgil Abloh/Off-White, featuring bold typography, quotation marks, and a minimalist black-and-white industrial design. The system is built to integrate with AutoCut's beat analysis and video editing workflows.

## User Preferences
- **Sovereignty:** All processing must remain local (no cloud transcription services)
- **Privacy:** No data leaks to external services
- **Design:** Virgil Abloh/Off-White aesthetic - quotation marks, bold typography, black/white minimalism, industrial styling
- **Integration focus:** Outputs designed for AutoCut beat analysis
- **Workflow:** Prototype on Replit → Export to Mac Mini → iPhone Shortcuts integration
- **Future project queued:** UI/UX design scraper tool (after DAWT-Transcribe complete)

## System Architecture

### UI/UX Decisions
The frontend UI is inspired by Virgil Abloh/Off-White, featuring:
- **Typography:** Bold Helvetica Neue, uppercase labels, tight letter-spacing.
- **Quotation Marks:** Decorative quotes around "TRANSCRIBE" heading.
- **Industrial Labels:** "AUDIO INPUT" cutout labels on bordered boxes.
- **Color Scheme:** Minimal black-on-white with a 4px black top stripe.
- **Buttons:** Black background with an arrow (→) indicator.
- **Segments:** Left-border emphasis, enhanced translations with arrow separator.
- **Spinners:** Square (no curves) for loading states.

### Technical Implementations
- **Backend:** FastAPI application with a Whisper + mT5 multilingual pipeline.
- **Async Processing:** Utilizes background job processing for transcriptions with browser notifications upon completion.
- **Data Persistence:** PostgreSQL database stores all transcription jobs and history.
- **Multilingual Enhancement:** mT5-small models (1.2GB) are used for 11 languages, with keyword detection and explicit language selection.
- **Transcription Editing:** Contenteditable UI for transcript and segment corrections, with export functionality for original-corrected pairs to build fine-tuning datasets.
- **AI-Friendly Exports:** Provides ChatGPT-ready markdown, clean markdown files, and structured JSON with metadata.
- **Robust API:** Includes request IDs, processing time metrics, structured error responses, and a `/health` endpoint.
- **Sovereignty:** All models (Whisper, mT5) run locally without external API calls, ensuring data privacy and control.
- **Video Length Protection:** Implements a 15-minute video length limit to prevent server overload.

### Feature Specifications
- **Input:** Accepts audio from URLs (TikTok, Instagram Reels, YouTube) or uploaded files.
- **Output:** Generates timestamped JSON, Markdown, and ChatGPT-ready text.
- **Language Support:** Auto-detects and supports specific African and European languages, including Pidgin, Twi, Igbo, Yoruba, Hausa, Swahili, Amharic, French, Portuguese, Ewe, and Dagbani, with forced language selection for Whisper.
- **Persistent History:** "My Transcripts" page provides one-click access to past jobs.

### System Design Choices
- **Excel DNA Principles:** Adheres to principles of resilience, local-first processing, sovereignty, and decades-long usability.
- **Modular Design:** Clear separation between frontend (static/index.html) and backend (main.py).
- **Graceful Fallback:** If machine translation fails, the system returns Whisper-only output without errors.

## External Dependencies
- **FastAPI:** Web framework for the backend API.
- **Uvicorn:** ASGI server.
- **openai-whisper:** Local Whisper model for transcription.
- **yt-dlp:** Used for downloading audio from social media platforms (TikTok, Instagram, YouTube).
- **transformers:** Hugging Face library for mT5 machine translation models.
- **torch:** PyTorch for machine learning model execution.
- **sentencepiece:** Tokenizer for mT5.
- **PostgreSQL:** Relational database for persistent storage of transcription jobs and history.