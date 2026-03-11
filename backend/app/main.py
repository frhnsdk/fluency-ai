from pathlib import Path
import tempfile
import os
import io

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.services.stt import speech_to_text
from app.services.ai import process_text
from app.services.tts import text_to_speech

BASE_DIR = Path(__file__).resolve().parent.parent  # /app
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Reply-Text"],
)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")


# ── In-memory session store ──────────────────────────────
sessions: dict[str, list[dict]] = {}


@app.get("/")
async def read_root():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.post("/stt")
async def stt_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".webm", ".mp3", ".m4a", ".ogg")):
        raise HTTPException(status_code=400, detail="Unsupported audio format")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        text = speech_to_text(tmp_path)
    finally:
        os.unlink(tmp_path)
    return {"text": text}


@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    text = data.get("text", "").strip()
    session_id = data.get("session_id", "default")

    if not text:
        raise HTTPException(status_code=400, detail="Empty text")

    if session_id not in sessions:
        sessions[session_id] = []

    history = sessions[session_id]
    reply = process_text(text, history)

    # Store conversation turn
    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": reply})

    # Generate TTS audio
    audio_bytes = text_to_speech(reply)

    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/wav",
        headers={"X-Reply-Text": reply.replace("\n", " ")},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)