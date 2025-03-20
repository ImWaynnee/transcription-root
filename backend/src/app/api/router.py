from fastapi import APIRouter
from app.api.http.routes import health, transcription

router = APIRouter()

# Include routers from endpoints without prefixes
router.include_router(health.router)
router.include_router(transcription.router)
