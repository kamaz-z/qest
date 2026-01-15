import subprocess
import sys
import time
import os
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BOT_FILE = "main.py"  # Твій бот

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_bot()

    def start_bot(self):
        if self.process:
            # Переконайся, що попередній процес закритий
            try:
                if os.name == 'nt':  # Windows
                    self.process.terminate()
                else:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except Exception:
                pass
        # Запуск нового процесу
        self.process = subprocess.Popen([sys.executable, BOT_FILE])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"\n[INFO] Файл {event.src_path} змінився. Перезапуск бота...")
            self.start_bot()


if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[INFO] Завершення роботи...")
        if event_handler.process:
            try:
                if os.name == 'nt':
                    event_handler.process.terminate()
                else:
                    os.killpg(os.getpgid(event_handler.process.pid), signal.SIGTERM)
            except Exception:
                pass
        observer.stop()

    observer.join()
