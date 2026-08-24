import queue
import time
from pathlib import Path
from typing import List, AsyncGenerator, Tuple, Dict
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEvent, FileCreatedEvent, FileModifiedEvent, FileDeletedEvent, \
  FileMovedEvent

from backend.src.library.Domain.data.notification import BookNotification
from backend.src.library.Infrastructure.observer.helpers.accumulator import WatchDogEventAccumulator


class WatchdogObserver:
  def __init__(
      self, observer = None
  ):
    self.observed_dirs = list()
    self.observer = observer or Observer()
    self.accumulator = WatchDogEventAccumulator()

  def set_observed_directories(
      self,
      directories: List[str]
  ) -> None:
    self._change_all_valid_directories(
      directories=directories
    )

  async def monitor_system(
      self
  ) -> AsyncGenerator[BookNotification, None]:
    self._observer_setup()
    self.observer.start()
    while self.observer.is_alive():
      events = await self.accumulator.accumulate_events(
        self.observer
      )
      upserts, deletes = self._classify_events(events)
      new_notification = self._make_new_notification(
        upserts = upserts,
        deletes = deletes
      )
      yield new_notification

  def _classify_events(
      self,
      events: List[FileSystemEvent]
  ) -> Tuple[Dict[str, str], Dict[str, str]]:
    upserts, deletes = dict(), dict()
    for event in events:
      event_location = Path(event.src_path)
      if isinstance(event, (FileCreatedEvent, FileModifiedEvent)):
        upserts[str(event_location.name)] = str(event_location.parent)
      if isinstance(event, (FileDeletedEvent, FileMovedEvent)):
        deletes[str(event_location.name)] = str(event_location.parent)
    return upserts, deletes

  def _make_new_notification(
      self,
      upserts: Dict[str, str],
      deletes: Dict[str, str]
  ) -> BookNotification:
    return BookNotification(
        timestamp = datetime.now(),
        events= {
          "upsert": upserts,
          "delete": deletes
        }
      )

  def _observer_setup(self):
    if not self.observed_dirs:
      raise ValueError("Directories not set up yet")
    event_handler = LoggingEventHandler()
    for directory in self.observed_dirs:
      self.observer.schedule(
        event_handler,
        directory,
        recursive = False
      )

  def _change_all_valid_directories(
      self,
      directories: List[str]
  ) -> None:
    self.observed_dirs.clear()
    if not directories:
      return
    for directory in directories:
      dir_as_path = Path(directory)
      if self._check_if_valid_directory(dir_as_path):
        self.observed_dirs.append(directory)


  def _check_if_valid_directory(
      self,
      dir_as_path: Path
  ) -> bool:
    if dir_as_path.is_dir():
      return True
    return False