import whisper
import numpy as np
from pyannote.audio import Pipeline

class Transcriber:
    def __init__(self, model_name="base"):
        print(f"Загрузка модели Whisper: {model_name}")
        self.model = whisper.load_model(model_name)

    def transcribe_audio(self, audio_chunk):
        """Транскрибирует аудио-чанк"""
        # Преобразование аудио в формат модели Whisper
        audio = self._preprocess_audio(audio_chunk)
        result = self.model.transcribe(audio, fp16=False)
        print ('Transcription is over. Diarization is in progress...')

        return result['text'], 

    def _preprocess_audio(self, audio_chunk):
        # Нормализация аудио
        audio = np.float32(audio_chunk) / 32768.0  # Преобразование int16 -> float32
        return audio
    
    