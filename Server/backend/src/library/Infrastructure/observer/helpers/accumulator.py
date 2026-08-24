from datetime import datetime
import queue
import time
from pathlib import Path
from typing import List, Tuple
from watchdog.observers import Observer

from watchdog.events import FileSystemEvent


class WatchDogEventAccumulator:
  async def accumulate_events(
      self,
      observer: Observer
  ) -> List[FileSystemEvent]:
    list_of_events = list()
    list_of_events, start_time = self._wait_for_first_event(
      observer = observer,
      list_of_events = list_of_events
    )
    list_of_events = self._check_for_following_events(
      observer=observer,
      start_time=start_time,
      list_of_events=list_of_events
    )
    return list_of_events

  @staticmethod
  def _wait_for_first_event(
      list_of_events: List[FileSystemEvent],
      observer: Observer
  ) -> Tuple[List[FileSystemEvent], float]:
    while True:
      first_event, _ = observer.event_queue.get()
      if Path(first_event.src_path).suffix in ['.pdf', '.epub']:
        list_of_events.append(first_event)
        start_time = time.perf_counter()
        break
    return list_of_events, start_time

  @staticmethod
  def _check_for_following_events(
      start_time: float,
      list_of_events: List[FileSystemEvent],
      observer: Observer
  ) -> List[FileSystemEvent]:
    try:
      while time.perf_counter() - start_time < 1.0:
        event, _ = observer.event_queue.get(timeout=1)
        if Path(event.src_path).suffix not in ['.pdf', '.epub']:
          continue
        list_of_events.append(event)
    except queue.Empty:
      pass
    finally:
      return list_of_events

