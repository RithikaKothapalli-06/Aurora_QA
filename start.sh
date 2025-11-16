#!/bin/bash

# Start the FastAPI app using Gunicorn + UvicornWorker
exec gunicorn main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT
