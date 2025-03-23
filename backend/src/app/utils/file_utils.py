import os
from fastapi import HTTPException

# Based on https://help.openai.com/en/articles/7031512-whisper-audio-api-faq
ALLOWED_AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.mp4', '.mpeg', '.mpga', '.webm'}

def validate_audio_file(filename: str) -> None:
    """Validate if the file has an allowed audio extension"""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed formats: {', '.join(ALLOWED_AUDIO_EXTENSIONS)}"
        )

def sanitize_filename(filename: str) -> str:
    """Remove extension and sanitize filename"""
    base_name = os.path.splitext(filename)[0]
    return base_name.strip().lower()
