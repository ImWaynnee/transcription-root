import os
from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.config import settings
from app.db.session import get_db
from app.api.http.controllers.transcription_controller import (
    transcribe_files,
    get_transcriptions,
    search_transcriptions
)

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

@router.get("/transcriptions", response_model=Dict[str, Any])
async def list_transcriptions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    """
    List all transcriptions with pagination
    """
    return get_transcriptions(page=page, limit=limit, db=db)

@router.get("/search", response_model=Dict[str, Any])
async def search_transcription_files(
    filename: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    """
    Search transcriptions by original filename with pagination
    """
    return search_transcriptions(filename=filename, page=page, limit=limit, db=db)
