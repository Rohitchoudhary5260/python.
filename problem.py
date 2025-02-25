import os
import time
import whisper
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
def scan_directory(directory):
    audio_video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp3', '.wav', '.mp4', '.mkv', '.mov', '.flv', '.aac', '.m4a')):
                audio_video_files.append(os.path.join(root, file))
    return audio_video_files
def transcribe_file(file_path, model):
    print(f'Transcribing {file_path}')
    result = model.transcribe(file_path)
    text_file_path = f'{file_path}.txt'
    with open(text_file_path, 'w') as f:
        f.write(result['text'])
    print(f'Transcription saved to {text_file_path}')
class Watcher:
    def __init__(self, directory, model):
        self.directory = directory
        self.event_handler = Handler(model)
        self.observer = Observer()

    def run(self):
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, model):
        self.model = model

    def on_created(self, event):
        if not event.is_directory:
            if event.src_path.endswith(('.mp3', '.wav', '.mp4', '.mkv', '.mov', '.flv', '.aac', '.m4a')):
                transcribe_file(event.src_path, self.model)
def main(directory):
    model = whisper.load_model("base")

    
    files = scan_directory(directory)
    for file in files:
        transcribe_file(file, model)

    
    watcher = Watcher(directory, model)
    watcher.run()

if __name__ == "__main__":
    main('C:\Users\rchou\OneDrive\Desktop\python')
