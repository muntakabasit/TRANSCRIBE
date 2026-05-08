#!/bin/zsh
set -euo pipefail

REPO_PATH="/Volumes/homelab/Storage/ofa_jack_agent/DAWT_Transcriber"
PYTHON_PATH="$REPO_PATH/.venv/bin/python"
export XDG_CACHE_HOME="$REPO_PATH/.cache"

cd "$REPO_PATH"
mkdir -p "$XDG_CACHE_HOME/whisper"
exec "$PYTHON_PATH" -m uvicorn main:app --app-dir "$REPO_PATH" --host 0.0.0.0 --port 5001
