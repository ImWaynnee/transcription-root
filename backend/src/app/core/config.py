import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Transcription Service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./data/transcriptions.db"
    UPLOAD_DIR: str = "uploads"
    MAX_CONCURRENT_PROCESSING: int = 10
    BACKEND_PORT: int = 8000  # Default backend port
    FRONTEND_PORT: int = 4550 # Default frontend port

    # Use our .env.test file if in testing environment.
    model_config: ConfigDict = ConfigDict(
        env_file=".env" if os.getenv("ENVIRONMENT") != "test" else ".env.test"
    )

settings = Settings()
