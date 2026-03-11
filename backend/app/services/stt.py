from app.models import whisper_model


def speech_to_text(audio_file: str) -> str:
    result = whisper_model.transcribe(audio_file)
    return result["text"]