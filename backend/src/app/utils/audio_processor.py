import os
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.config import settings
from app.models.transcription import Transcription
from app.services.service_container import whisper_service
from app.utils.text_processor import clean_transcription
from app.utils.file_utils import validate_audio_file, sanitize_filename

MAX_FILE_SIZE_MB = 25

def get_base_filename(filename: str) -> str:
    """
    Get the base filename without the extension
    """
    return os.path.splitext(filename)[0]

async def process_audio_file(file: UploadFile, db: Session):
    """
    Process and transcribe an audio file
    """
    validate_audio_file(file.filename)

    # Check file size
    file_size_mb = len(await file.read()) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB}MB"
        )

    # Reset file read position
    await file.seek(0)

    original_filename = file.filename
    base_name = get_base_filename(original_filename)
    sanitized_name = sanitize_filename(base_name)

    # Check if file already exists (case-insensitive)
    existing = db.query(Transcription).filter(
        func.lower(Transcription.sanitized_filename) == sanitized_name.lower()
    ).first()

    file_path = os.path.join(settings.UPLOAD_DIR, original_filename)

    try:
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        raw_transcription = await whisper_service.transcribe(file_path)
        cleaned_transcription = clean_transcription(raw_transcription)

        if existing:
            # Update existing entry
            existing.transcribed_text = cleaned_transcription
            db.commit()
            db.refresh(existing)
            return {
                "filename": base_name,
                "transcription": cleaned_transcription
            }
        else:
            # Create new entry
            db_transcription = Transcription(
                filename=base_name,
                sanitized_filename=sanitized_name,
                transcribed_text=cleaned_transcription
            )
            db.add(db_transcription)
            db.commit()
            db.refresh(db_transcription)
            return {
                "filename": base_name,
                "transcription": cleaned_transcription
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
