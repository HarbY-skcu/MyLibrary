import queue
from abc import ABC
from pathlib import Path
from time import sleep
from typing import Tuple, Protocol, List

from watchdog.events import FileSystemEvent, FileCreatedEvent, FileModifiedEvent
from watchdog.observers import Observer

class MockedEventQueueRequirements(Protocol):
  random_events: List[FileSystemEvent]

class MockedEventQueue(MockedEventQueueRequirements, ABC):
  def get(
      self,
      timeout: float = None
  ) -> Tuple[FileSystemEvent, None]:
    if timeout and not self.random_events:
      sleep(timeout)
      raise queue.Empty
    event = self.random_events.pop()
    return event, None

class MockedObserver():
  def __init__(
      self,
      event_queue: MockedEventQueue
  ):
    self.event_queue = event_queue

  def start(self) -> None:
    pass

  def is_alive(self) -> bool:
    return True

class MockedEventQueueWithUpserts(MockedEventQueue):
  def __init__(self):
    self.random_events = [
      FileCreatedEvent(
        src_path= str(Path("../../sample data/all books/cc-shared-culture.epub").resolve())
      ),
      FileModifiedEvent(
        src_path= str(Path("../../sample data/all books/minimal-document.pdf").resolve())
      )
    ]

class MockedEventQueueWithNonBookFiles(MockedEventQueue):
  def __init__(self):
    self.random_events = [
      FileCreatedEvent(
        src_path= str(Path("../../sample data/no books/Alices Adventures in Wonderland.azw3").resolve)
      ),
      FileModifiedEvent(
        src_path= str(Path("../../sample data/no books/sample2.html").resolve())
      )
    ]

class MockedEventQueueWithMixedFiles(MockedEventQueue):
  def __init__(self):
    self.random_events = [
      FileCreatedEvent(
        src_path=str(Path("../../sample data/no books/Alices Adventures in Wonderland.azw3").resolve)
      ),
      FileCreatedEvent(
        src_path=str(Path("../../sample data/all books/cc-shared-culture.epub").resolve())
      ),
      FileModifiedEvent(
        src_path=str(Path("../../sample data/no books/sample2.html").resolve())
      ),
      FileModifiedEvent(
        src_path=str(Path("../../sample data/all books/minimal-document.pdf").resolve())
      )
    ]