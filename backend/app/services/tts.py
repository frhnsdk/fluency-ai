import tempfile
import os
import pyttsx3


def text_to_speech(text: str) -> bytes:
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp_path = tmp.name
    try:
        engine.save_to_file(text, tmp_path)
        engine.runAndWait()
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        os.unlink(tmp_path)