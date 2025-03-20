from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from typing import Dict

class WhisperService:
    def __init__(self):
        self.is_ready = False
        self.processor = None
        self.model = None
        self.initialize_models()

    def initialize_models(self):
        try:
            self.processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
            self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
            self.is_ready = True
        except Exception as e:
            self.is_ready = False
            self.error = str(e)

    def check_health(self) -> Dict:
        return {
            "service": "whisper",
            "status": "ready" if self.is_ready else "not_ready",
            "error": self.error if not self.is_ready else None
        }

    async def transcribe(self, file_path: str) -> str:
        if not self.is_ready:
            raise Exception("Whisper service is not ready")

        # Load audio file
        audio, sr = librosa.load(file_path, sr=16000)
        
        # Process audio with Whisper
        input_features = self.processor(
            audio, 
            sampling_rate=16000, 
            return_tensors="pt"
        ).input_features

        predicted_ids = self.model.generate(input_features)
        return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0] 