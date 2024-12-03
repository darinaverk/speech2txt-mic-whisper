import cv2
import pyaudio
import numpy as np

class VideoCapture:
    def __init__(self, rate=16000, chunk=1024, channels=1):
        self.rate = rate
        self.chunk = chunk
        self.channels = channels

        # Инициализация видео
        self.cap = cv2.VideoCapture(0)

        # Инициализация аудио
        self.audio_stream = pyaudio.PyAudio().open(
            #input=True,
            
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

    def get_audio_chunk(self):
        """Возвращает аудио-чанк"""
        audio_data = self.audio_stream.read(self.chunk)
        return np.frombuffer(audio_data, dtype=np.int16)

    def get_video_frame(self):
        """Возвращает кадр видео"""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.cap.release()
        self.audio_stream.stop_stream()
        self.audio_stream.close()