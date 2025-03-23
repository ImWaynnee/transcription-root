from pydantic import BaseModel, ConfigDict

# Public Schema for transcriptions
class TranscriptionResponse(BaseModel):
    id: int
    filename: str
    transcription: str

    model_config = ConfigDict(from_attributes=True)
