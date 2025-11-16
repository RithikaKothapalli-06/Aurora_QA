#!/bin/bash

# Ensure PORT is set
export PORT=${PORT:-8000}

# Start FastAPI using Gunicorn + Uvicorn worker
exec gunicorn main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT

