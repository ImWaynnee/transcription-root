from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Dict
from app.services.whisper_service import WhisperService

router = APIRouter()
whisper_service = WhisperService()

@router.get("/health")
async def health_check() -> Dict:
    """
    Check the health of all services
    """
    whisper_status = whisper_service.check_health()
    
    return {
        "timestamp": datetime.now(),
        "services": {
            "api": {
                "status": "healthy"
            },
            "whisper": whisper_status
        }
    } 