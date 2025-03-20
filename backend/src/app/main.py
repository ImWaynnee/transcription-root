import logging
from fastapi import FastAPI
from app.api.router import router
from app.db.session import init_db
from app.core.config import settings
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

init_db()

app = FastAPI(title="Transcription Service")

# Include all routes without any prefix
app.include_router(router, prefix="")  # explicitly set no prefix 

# Post-startup logging
logging.info("---------------------------")
logging.info("Instance successfully started")
logging.info(f"Listening on port {settings.PORT}")
logging.info(f"Timestamp: {datetime.now()}")
logging.info("---------------------------")