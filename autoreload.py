# autoreload.py
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, files_to_watch, command):
        self.files_to_watch = files_to_watch
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.process = subprocess.Popen([sys.executable, self.command])

    def on_modified(self, event):
        for file in self.files_to_watch:
            if event.src_path.endswith(file):
                print(f"{file} changed, reloading...")
                self.start_process()
                break

if __name__ == "__main__":
    files = ["run.py", "config.py", "data_loader.py", "ai_core.py"]
    event_handler = ReloadHandler(files, "run.py")
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    print(f"Watching {', '.join(files)} for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    if event_handler.process:
        event_handler.process.terminate()
