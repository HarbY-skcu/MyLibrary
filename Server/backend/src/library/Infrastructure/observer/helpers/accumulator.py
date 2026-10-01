import asyncio
from datetime import datetime
import queue
import time
from pathlib import Path
from typing import List, Tuple
from watchdog.observers import Observer

from watchdog.events import FileSystemEvent


class WatchDogEventAccumulator:
  def __init__(
      self,
      first_event_timeout: float = None
  ):
    self.first_event_timeout = first_event_timeout

  async def accumulate_events(
      self,
      event_queue: queue.Queue
  ) -> List[FileSystemEvent]:
    list_of_events = list()
    list_of_events, start_time = await asyncio.to_thread(
      self._wait_for_first_event,
      list_of_events=list_of_events,
      event_queue = event_queue,
      first_event_timeout = self.first_event_timeout
    )
    list_of_events = self._check_for_following_events(
      event_queue = event_queue,
      start_time=start_time,
      list_of_events=list_of_events
    )
    return list_of_events

  @staticmethod
  def _wait_for_first_event(
      list_of_events: List[FileSystemEvent],
      event_queue: queue.Queue,
      first_event_timeout: float | None
  ) -> Tuple[List[FileSystemEvent], float]:
    start_time = time.perf_counter()
    while True:
      if (
        first_event_timeout is not None
        and time.perf_counter() - start_time > first_event_timeout
      ):
        break
      try:
        first_event, _ = event_queue.get(timeout=1)
        if Path(first_event.src_path).suffix in ['.pdf', '.epub']:
          list_of_events.append(first_event)
          start_time = time.perf_counter()
          break
      except queue.Empty:
        pass
    return list_of_events, start_time

  @staticmethod
  def _check_for_following_events(
      start_time: float,
      list_of_events: List[FileSystemEvent],
      event_queue,
  ) -> List[FileSystemEvent]:
    try:
      while time.perf_counter() - start_time < 1.0:
        event, _ = event_queue.get(timeout=1)
        if Path(event.src_path).suffix not in ['.pdf', '.epub']:
          continue
        list_of_events.append(event)
    except queue.Empty:
      pass
    return list_of_events

