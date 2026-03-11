# English Speaking Bot

A fully offline English speaking bot using Python + FastAPI, HTML/CSS/JS with Bootstrap, deployed in Docker.

## Features

- Speech to Text: Whisper
- AI Processing: Mistral 7B for grammar correction, synonyms, and conversational replies
- Text to Speech: Qwen3 TTS
- In-memory session history
- Chat interface
- Loops until "Thank you bye"

## Setup

1. Build Docker image: `docker build -t speaking-bot .`
2. Run container: `docker run -p 8000:8000 speaking-bot`
3. Open browser to http://localhost:8000

## Requirements

- Docker
- Sufficient RAM/GPU for models