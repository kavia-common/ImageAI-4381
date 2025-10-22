#!/usr/bin/env sh
# PUBLIC_INTERFACE
# start-backend.sh
# Purpose: Start the FastAPI backend server for preview environments.
# This script sets a default PORT (3001) if not provided and runs uvicorn
# pointing to the FastAPI app defined in backend/app/main.py.

set -e

PORT="${PORT:-3001}"
HOST="0.0.0.0"

echo "Starting ImageAI backend on ${HOST}:${PORT} ..."
exec uvicorn backend.app.main:app --host "${HOST}" --port "${PORT}"
