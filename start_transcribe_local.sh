#!/bin/zsh
set -euo pipefail

REPO_PATH="/Users/kulturestudios/ofa_jack_agent/projects/dawt_transcribe"
PYTHON_PATH="$REPO_PATH/.venv/bin/python"
export XDG_CACHE_HOME="$REPO_PATH/.cache"

# Homebrew tools (ffmpeg, etc.) are not in launchd's default PATH.
# Whisper needs ffmpeg to decode audio files (especially webm/opus from yt_dlp).
export PATH="/opt/homebrew/bin:$PATH"

cd "$REPO_PATH"
mkdir -p "$XDG_CACHE_HOME/whisper"
exec "$PYTHON_PATH" -m uvicorn main:app --app-dir "$REPO_PATH" --host 0.0.0.0 --port 5001
