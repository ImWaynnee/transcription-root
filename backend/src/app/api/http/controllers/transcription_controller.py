from fastapi import UploadFile, Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import asyncio

from app.db.session import get_db
from app.core.config import settings
from app.models.transcription import Transcription
from app.schemas.transcription import TranscriptionResponse
from app.utils.audio_processor import process_audio_file
from app.utils.pagination import paginate_query

router = APIRouter()

async def transcribe_files(
    files: List[UploadFile],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Handle file uploads and return transcriptions.
    """
    # Check for duplicate filenames
    filenames = [file.filename for file in files]
    if len(filenames) != len(set(filenames)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate filenames detected in the request payload"
        )

    # Create a semaphore to limit concurrent processing
    semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_PROCESSING)

    async def process_with_semaphore(file: UploadFile) -> Dict:
        async with semaphore:
            try:
                return await process_audio_file(file, db)
            except Exception as e:
                return {
                    "filename": file.filename,
                    "error": str(e)
                }

    # Process files concurrently with semaphore limit
    results = await asyncio.gather(
        *[process_with_semaphore(file) for file in files]
    )

    return {
        "total": len(files),
        "successful": len([r for r in results if "error" not in r]),
        "results": results
    }

def get_transcriptions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Return all transcriptions.
    """
    query = db.query(Transcription)
    paginated_data = paginate_query(query, page, limit)
    paginated_data["results"] = [
        TranscriptionResponse(
            id=transcription.id,
            filename=transcription.filename,
            transcription=transcription.transcribed_text
        )
        for transcription in paginated_data["results"]
    ]
    return paginated_data

def search_transcriptions(
    filename: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Return transcriptions filtered by filename provided.
    """
    query = db.query(Transcription).filter(
        Transcription.filename.ilike(f"%{filename}%")
    )
    paginated_data = paginate_query(query, page, limit)
    paginated_data["results"] = [
        TranscriptionResponse(
            id=transcription.id,
            filename=transcription.filename,
            transcription=transcription.transcribed_text
        )
        for transcription in paginated_data["results"]
    ]
    return paginated_data
