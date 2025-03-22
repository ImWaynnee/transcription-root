from pydantic import BaseModel, ConfigDict

class TranscriptionResponse(BaseModel):
    id: int
    filename: str
    transcription: str

    model_config = ConfigDict(from_attributes=True)
