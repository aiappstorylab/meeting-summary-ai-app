import torch
from faster_whisper import WhisperModel
import os

class STTService:
    def __init__(self):
        # Auto-detect hardware
        if torch.cuda.is_available():
            self.device = "cuda"
            self.compute_type = "float16"
        else:
            self.device = "cpu"
            self.compute_type = "int8"
        
        print(f"STT Model initialized on {self.device} with {self.compute_type}")
        # Use base model for balance between speed and quality
        self.model = WhisperModel("base", device=self.device, compute_type=self.compute_type)

    async def transcribe(self, file_path: str) -> str:
        segments, info = self.model.transcribe(file_path, beam_size=5, language="ko")
        
        full_text = []
        for segment in segments:
            full_text.append(segment.text)
            
        return " ".join(full_text)

# Singleton instance
stt_service = STTService()
