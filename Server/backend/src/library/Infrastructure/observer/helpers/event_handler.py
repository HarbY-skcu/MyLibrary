from watchdog.events import FileSystemEventHandler
from queue import Queue

class EventHandlerWithQueue(FileSystemEventHandler):
    def __init__(self, my_queue: Queue):
        super().__init__()
        self.my_queue = my_queue

    def on_any_event(self, event):
        self.my_queue.put_nowait(event)