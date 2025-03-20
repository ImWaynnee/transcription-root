from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base_class import Base

class Transcription(Base):
    __tablename__ = 'transcriptions'

    id = Column(Integer, primary_key=True, index=True)  # Our Primary Key
    filename = Column(String, unique=True, index=True)  # Original filename for searching
    sanitized_filename = Column(String, unique=True, index=True)  # Sanitized filename to prevent duplicates
    transcribed_text = Column(String)   # The transcribed text
    created_at = Column(DateTime, default=datetime.now) # Creation timestamp