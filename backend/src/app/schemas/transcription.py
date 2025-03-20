from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    id: int
    filename: str
    transcription: str

    class Config:
        orm_mode = True 