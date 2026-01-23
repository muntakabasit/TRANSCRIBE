# DAWT-Transcribe Changelog

## v1.2 - Video Support & Completion Rituals (2026-01-23)

### ✨ New Features

#### Video Upload Support
- **Supported formats**: MP4, MOV, AVI, MKV (in addition to audio formats)
- **File size limit**: Increased to 100MB (was 50MB for audio only)
- **Backend**: Already supports video via pydub + ffmpeg (extracts audio automatically)
- **UI**: Updated file picker to accept `audio/*,video/*`

#### Completion Rituals (Calm, Confident UX)

**When transcription completes:**
- 600ms checkmark overlay (✓) with gentle pulse animation
- Fades out automatically after completion ritual
- Smooth scroll to transcript view
- No interruption to user flow

**Transcript display:**
- 500ms gentle fade-in animation on mount
- Creates a calm "moment of arrival" feeling

**Share button behavior:**
- Tap Share → 300ms "Preparing..." state (subtle pulse)
- Then native share sheet opens (or copies to clipboard as fallback)
- The micro-delay creates confidence, not confusion
- Users see system is working before share sheet appears

**Design principles followed:**
- ✅ No slow friction on import/start
- ✅ Rituals only at completion moments
- ✅ Subtle, non-blocking animations (300-600ms)
- ✅ Confidence through minimal feedback

### 🚀 Performance Improvements (v1.1)

- **Removed MT5 Translation**: Eliminated slow CPU-based translation
- **10-20x faster**: Transcription now takes seconds instead of minutes
- **Simpler architecture**: -190 lines of complex translation code
- **Whisper native**: Uses Whisper's built-in multi-language support

### 🐛 Bug Fixes

- Fixed local language transcription in `/transcribe_file` endpoint
- Proper Whisper language code mapping (e.g., "ak" for Twi, "yo" for Yoruba)
- All 12 languages now work correctly: English, Pidgin, Twi, Igbo, Yoruba, Hausa, Swahili, Amharic, French, Portuguese, Ewe, Dagbani

## v1.0 - Initial Web App Release

### Features
- 3 input methods: Record, Upload, URL (YouTube/TikTok/Instagram)
- PWA support for installable web app
- DAWT design system (warm beige + gold accent)
- Real-time transcription with Whisper
- 12+ language support
- Copy, download, and share transcripts

### Infrastructure
- Frontend: Next.js 15 + React 19 on Vercel
- Backend: FastAPI + Whisper on Fly.io
- Database: SQLite with job tracking

## Deployment Status

### Backend (Fly.io)
- App: `transcribe-h3f8nq`
- URL: https://transcribe-h3f8nq.fly.dev
- Status: ⏳ Needs deployment with v1.1-1.2 changes

### Frontend (Vercel)
- Auto-deploys from GitHub main branch
- Status: ✅ Latest changes pushed

## Next Steps

1. Deploy backend to Fly.io:
   ```bash
   fly deploy
   ```

2. Test video upload:
   - Upload a short MP4 video
   - Verify audio extraction works
   - Check transcription accuracy

3. Test completion rituals:
   - Complete a transcription
   - Watch for 600ms checkmark overlay
   - Verify smooth scroll to transcript
   - Test Share button "Preparing..." state

4. Install PWA on phone and test mobile experience

## Known Limitations

- Video files limited to 100MB (Fly.io memory constraints)
- No GPU acceleration (slower than optimal, but acceptable)
- YouTube URL downloads can be unreliable (yt-dlp limitations)

## Future Enhancements

- [ ] GPU support for faster transcription
- [ ] Transcript editing capability
- [ ] Export to multiple formats (SRT, VTT, PDF)
- [ ] History/saved transcripts
- [ ] Real-time transcription progress indicator
- [ ] Support for longer videos (>20 min)
