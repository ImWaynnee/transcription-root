from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Transcription Service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./data/transcriptions.db"
    UPLOAD_DIR: str = "uploads"
    MAX_CONCURRENT_PROCESSING: int = 10
    BACKEND_PORT: int = 8000  # Default backend port
    FRONTEND_PORT: int = 4550 # Default frontend port
    class Config:
        env_file = ".env"

settings = Settings()
