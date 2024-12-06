import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from persistqueue import Queue
from message_processor import (
    SignalHandler,
    logger,
    RAW_MOUNT_POINT,
    process_message,
)
LEN = len(os.path.abspath(RAW_MOUNT_POINT))
queue_dir = os.path.join(os.path.dirname(__file__), 'queue_dir')

if not os.path.exists(queue_dir):
    os.makedirs(queue_dir)
    
file_queue = Queue(queue_dir)

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            abs_path = os.path.abspath(event.src_path)
            src_path = abs_path[LEN:]
            logger.info(f"File got created: {src_path}")
            file_queue.put(src_path) # Put path to queue instead of process_message() directly

# add queue
def process_queue():
    while not file_queue.empty():
        src_path = file_queue.get()
        try: # try-catch just incase something fails, probably never
            logger.info(f"Processing audio file: {src_path}")
            process_message(src_path)
        except Exception as e:
            logger.error(f"Error processing file {src_path}: {e}")
        finally:
            file_queue.task_done() # On fail or no fail, skip the thing!

# TODO fix signal handling

def watch_directory():
    signal_handler = SignalHandler()
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=RAW_MOUNT_POINT, recursive=True)
    observer.start()

    try:
        while not signal_handler.received_signal:
            time.sleep(1)
            process_queue()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch_directory()