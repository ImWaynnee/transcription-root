import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
from app.db.session import init_db
from app.core.config import settings
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

init_db()

app = FastAPI(title=settings.PROJECT_NAME)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{settings.FRONTEND_PORT}"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes without any prefix
app.include_router(router, prefix="")  # explicitly set no prefix

# Post-startup logging
logging.info("---------------------------")
logging.info("Instance successfully started")
logging.info(f"Listening on port {settings.BACKEND_PORT}")
logging.info(f"Timestamp: {datetime.now()}")
logging.info("---------------------------")
