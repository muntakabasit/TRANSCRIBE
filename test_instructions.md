# How to Test DAWT-Transcribe v2.3.1

## Quick Test Instructions

1. **Visit the app**: http://localhost:5000

2. **Find a short video** (<10 minutes):
   - **Twi videos**: Search YouTube for "Twi news Ghana" or "Twi language lesson"
   - **Pidgin videos**: Search YouTube for "Nigerian Pidgin comedy" or "Mark Angel Comedy"

3. **Test the language forcing**:
   - Paste the YouTube URL
   - Select the correct language (Twi, Pidgin, etc.)
   - Click "PROCESS"
   
4. **What you'll see**:
   - Job submits instantly
   - Check `/status/job_XXXXX` for progress
   - Results will include version metadata:
     ```json
     {
       "meta": {
         "version": "2.3.0",
         "format": "dawt-transcript-v1",
         "compatible_since": "2.0.0"
       },
       "full_text": "...",
       "segments": [...]
     }
     ```

5. **Verify the fix**:
   - Twi videos should transcribe in Twi (not Arabic!)
   - Whisper is forced to use your selected language
   - No more auto-detection errors

## Example Channels to Test:
- **Twi**: LEARNAKAN, Joy TV, GhanaWeb
- **Pidgin**: Mark Angel Comedy, Broda Shaggi, YAWA Skits
