import pyaudio
import wave
import speech_recognition as sr
import subprocess
import keyboard
import threading
import time
import io

class WinVoiceToText:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        
        print("=== Режим: Удерживай [2] ===")
        print("Запись идет, пока кнопка нажата. Отпусти — распознаю.")
        print("Нажми [Esc] для выхода.")

    def record_audio(self):
        # Настройки аудиопотока
        stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=1024)
        frames = []
        
        # Записываем, пока нажата клавиша
        while keyboard.is_pressed('2'):
            data = stream.read(1024)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        
        # Собираем аудио в формат, понятный библиотеке SpeechRecognition
        raw_data = b''.join(frames)
        audio_file = sr.AudioData(raw_data, 16000, 2)
        return audio_file

    def recognize_and_copy(self, audio_data):
        print("⏳ Распознавание...")
        try:
            text = self.recognizer.recognize_google(audio_data, language="ru-RU")
            print(f"✓ {text}")
            subprocess.run(["clip.exe"], input=text.encode("utf-16le"), check=True)
            print("📋 Скопировано!")
        except Exception as e:
            print(f"❌ Ошибка или тишина: {e}")

    def run(self):
        while not keyboard.is_pressed('esc'):
            if keyboard.is_pressed('2'):
                audio = self.record_audio()
                self.recognize_and_copy(audio)
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        app = WinVoiceToText()
        app.run()
    finally:
        app.p.terminate()
