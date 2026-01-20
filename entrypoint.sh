#!/bin/bash
set -e

echo "=========================================="
echo "DAWT-Transcribe Startup Script"
echo "=========================================="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Files in current directory:"
ls -la
echo "=========================================="

echo "Testing Python imports..."
python -c "import main; print('✅ Main module imported successfully')"

echo "=========================================="
echo "Starting uvicorn server..."
echo "Host: 0.0.0.0"
echo "Port: 8080"
echo "=========================================="

exec uvicorn main:app --host 0.0.0.0 --port 8080 --log-level info
