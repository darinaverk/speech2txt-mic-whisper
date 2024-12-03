from video_capture import VideoCapture
#from diarization import SpeakerDiarization
from app import launch_gradio_interface


from transcriber___ import Transcriber

def main():
    # Инициализация потоков
    video_stream = VideoCapture()
    transcriber = Transcriber()
    
    print("Запуск приложения транскрибации...")
    try:
        # Запускаем веб-приложение с Gradio
        launch_gradio_interface()
    except KeyboardInterrupt:
        print("\nОстановка приложения.")
    finally:
        video_stream.release()

if __name__ == "__main__":
    main()