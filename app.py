import gradio as gr
import numpy as np
from video_capture import VideoCapture
from transcriber___ import Transcriber
from datetime import datetime
import threading
import time


def launch_gradio_interface():
    # Инициализация видеопотока и модели транскрибации
    video_stream = VideoCapture()
    transcriber = Transcriber()

    # Переменные для управления состоянием
    is_recording = [False]  # Состояние записи
    audio_buffer = []  # Буфер для накопления аудио
    sample_rate = 16000  # Частота дискретизации
    buffer_duration = 60 * sample_rate  # Длительность записи для обработки (60 секунд)
    last_save_time = [datetime.now()]  # Последнее время сохранения данных
    transcription_text = [""]  # Хранение текста транскрипции

    # Путь для файла транскрипции
    transcription_file_path = "transcription.txt"

    def start_recording():
        """
        Начинает запись аудио.
        """
        if is_recording[0]:
            return "Запись уже идет..."
        is_recording[0] = True
        #audio_buffer.clear()  # Очистка буфера для новой записи
        return "Запись начата. Говорите в микрофон."

    def stop_recording():
        """
        Останавливает запись.
        """
        if not is_recording[0]:
            return "Запись не была начата."
        is_recording[0] = False
        return "Запись остановлена."

    def save_and_process_audio():
        """
        Обрабатывает накопленный звуковой буфер каждые 60 секунд.
        """
        if not audio_buffer:
            return "No, buffer"

        # Конкатенация аудио буфера
        total_audio = np.concatenate(audio_buffer) if audio_buffer else np.array([])
        audio_buffer.clear()  # Очистка буфера после сохранения

        # Выполнение транскрибации
        try:
            text = transcriber.transcribe_audio(total_audio)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Добавление текста в глобальную переменную
            transcription_text[0] += f"[{timestamp}] {text}\n"

            # Запись текста в файл
            with open(transcription_file_path, "a", encoding="utf-8") as text_file:
                text_file.write(f"[{timestamp}] {text}\n")

            print(f"[{timestamp}] Данные сохранены.")
        except Exception as e:
            print(f"Ошибка обработки аудио: {e}")

    def process_audio():
        """
        Захватывает аудиофрагменты, если запись идет.
        """
        if not is_recording[0]:
            return

        # Захват аудио
        audio_chunk = video_stream.get_audio_chunk()
        if audio_chunk is not None and len(audio_chunk) > 0:
            audio_buffer.append(audio_chunk)

        # Проверяем, прошла ли минута с момента последнего сохранения
        current_time = datetime.now()
        if (current_time - last_save_time[0]).total_seconds() >= 120:
            save_and_process_audio()
            last_save_time[0] = current_time
            #audio_buffer.clear()  # Очистка буфера после сохранения

    def read_file():
        with open('transcription.txt', 'r', encoding='utf-8') as file:
            return file.read()
        
    def update_text():
        while True:
            with open('transcription.txt', 'r', encoding='utf-8') as file:
                text = file.read()
            yield text
            time.sleep(2)
    # Gradio интерфейс

    with gr.Blocks() as app:
        gr.Markdown("### Транскрибация аудио с записью каждые 60 секунд")

        # Кнопки управления и поле для текста
        with gr.Row():
            start_btn = gr.Button("Начать запись")
            stop_btn = gr.Button("Остановить запись")
        with gr.Row():
            text_output = gr.Textbox(label="Результат транскрибации", lines=10)
            app.load(update_text, inputs=None, outputs=text_output)
            #timer_display = gr.Label(value="Таймер: 60 секунд")

        # Связываем кнопки с функциями
        start_btn.click(fn=start_recording)
        stop_btn.click(fn=stop_recording)

    # Gradio интерфейс
    ''''with gr.Blocks() as app:
        gr.Markdown("### Транскрибация аудио с записью каждые 60 секунд")

        # Кнопки управления и поле для текста
        with gr.Row():
            start_btn = gr.Button("Начать запись")
            stop_btn = gr.Button("Остановить запись")
        text_output = gr.Textbox(label="Результат транскрибации", lines=20)

        # Функция для обновления текстового поля
        def update_textbox():
            """
            Обновляет текстовое поле в интерфейсе.
            """
            return transcription_text[0]

        # Связываем кнопки с функциями
        start_btn.click(fn=start_recording, outputs=text_output)
        stop_btn.click(fn=stop_recording, outputs=text_output)

        # Поток для регулярного обновления текста
        'def periodic_update():
            while True:
                if is_recording[0]:
                    # Обновление текстового поля
                    text_output.value = transcription_text[0]
                time.sleep(5)  # Обновление каждые 2 секунды'''

        # Запуск потока для обновления текста
        #threading.Thread(target=periodic_update, daemon=True).start()'''''''

    # Циклический захват аудио
    def audio_loop():
        while True:
            #save_and_process_audio()
            process_audio()

    threading.Thread(target=audio_loop, daemon=True).start()
    #record_thread = threading.Thread(target=save_and_process_audio, daemon=True)
    #process_thread = threading.Thread(target=process_audio, daemon=True)


    app.launch()