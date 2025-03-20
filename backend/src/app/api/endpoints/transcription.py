import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.config import settings
from app.db.session import get_db
from app.controllers.transcription_controller import (
    transcribe_files,
    index_transcriptions,
    search_transcriptions
)
from app.schemas.transcription import TranscriptionResponse

router = APIRouter()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe")
async def transcribe_audio(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Transcribe one or multiple audio files
    """
    return await transcribe_files(files, db)

@router.get("/transcriptions", response_model=List[TranscriptionResponse])
async def get_transcriptions(db: Session = Depends(get_db)):
    """
    List all transcriptions with selected fields
    """
    transcriptions = index_transcriptions(db)
    return [
        TranscriptionResponse(
            id=transcription.id,
            filename=transcription.filename,
            transcription=transcription.transcribed_text
        )
        for transcription in transcriptions
    ]

@router.get("/search", response_model=List[TranscriptionResponse])
async def search_transcription_files(
    filename: str,
    db: Session = Depends(get_db)
):
    """
    Search transcriptions by original filename
    """
    return search_transcriptions(filename, db) 