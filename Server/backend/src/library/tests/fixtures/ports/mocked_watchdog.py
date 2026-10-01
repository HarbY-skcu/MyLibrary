import queue
from abc import ABC
from pathlib import Path
from time import sleep
from typing import Tuple, Protocol, List

import pytest
from watchdog.events import FileSystemEvent, FileCreatedEvent, FileModifiedEvent, FileDeletedEvent, FileMovedEvent
from watchdog.observers import Observer

class MockedObserver():
  def __init__(
      self,
      event_queue: queue.Queue
  ):
    self.event_queue = event_queue


  def start(self) -> None:
    pass

  def is_alive(self) -> bool:
    return True

@pytest.fixture
def upsert_events(
) -> List[Tuple[FileSystemEvent, str]]:
  return [
    (
      FileCreatedEvent(
        src_path= str(Path("../../sample data/all books/cc-shared-culture.epub").resolve()),
      ),
      ""
    ),
    (
      FileModifiedEvent(
        src_path=str(Path("../../sample data/all books/minimal-document.pdf").resolve())
      ),
      ""
    )
  ]

@pytest.fixture
def delete_events(
) -> List[Tuple[FileSystemEvent, str]]:
  return [
    (
      FileMovedEvent(
        src_path = str(Path("../../sample data/all books/cc-shared-culture.epub").resolve())
      ),
      ""
    ),
    (
      FileDeletedEvent(
        src_path=str(Path("../../sample data/all books/minimal-document.pdf").resolve())
      ),
      ""
    )
  ]

@pytest.fixture
def events_with_non_book_files(
) -> List[Tuple[FileSystemEvent, str]]:
  return [
    (
      FileCreatedEvent(
        src_path=str(Path("../../sample data/no books/Alices Adventures in Wonderland.azw3").resolve)
      ),
      ""
    ),
    (
      FileModifiedEvent(
        src_path=str(Path("../../sample data/no books/sample2.html").resolve())
      ),
      ""
    )
  ]

@pytest.fixture
def mixed_file_type_events(
) -> List[Tuple[FileSystemEvent, str]]:
  return [
    (
      FileCreatedEvent(
        src_path=str(Path("../../sample data/no books/Alices Adventures in Wonderland.azw3").resolve)
      ),
      ""
    ),
    (
      FileCreatedEvent(
        src_path=str(Path("../../sample data/all books/cc-shared-culture.epub").resolve())
      ),
      ""
    ),
    (
      FileModifiedEvent(
        src_path=str(Path("../../sample data/no books/sample2.html").resolve())
      ),
      ""
    ),
    (
      FileModifiedEvent(
        src_path=str(Path("../../sample data/all books/minimal-document.pdf").resolve())
      ),
      ""
    )
  ]

@pytest.fixture
def mocked_event_queue_with_mixed_files(
  mixed_file_type_events: List[FileSystemEvent]
) -> queue.Queue:
  event_queue = queue.Queue()
  for event in mixed_file_type_events:
    event_queue.put(event)
  return event_queue

@pytest.fixture
def mocked_event_queue_with_upsets(
  upsert_events: List[FileSystemEvent]
) -> queue.Queue:
  event_queue = queue.Queue()
  for event in upsert_events:
    event_queue.put(event)
  return event_queue

@pytest.fixture
def mocked_event_queue_with_deletes(
  delete_events: List[FileSystemEvent]
) -> queue.Queue:
  event_queue = queue.Queue()
  for event in delete_events:
    event_queue.put(event)
  return event_queue

@pytest.fixture
def mocked_event_queue_with_unwanted_files(
  events_with_non_book_files: List[FileSystemEvent]
) -> queue.Queue:
  event_queue = queue.Queue()
  for event in events_with_non_book_files:
    event_queue.put(event)
  return event_queue