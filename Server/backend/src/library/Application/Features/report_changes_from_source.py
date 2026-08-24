from typing import Dict, AsyncGenerator

from backend.src.library.Application.ports.observer import Observer
from asyncio import LifoQueue

class ReportChangesFromSourceFeature:

  def __init__(
      self,
      book_observer: Observer,
  ):
    self.observer = book_observer
    self._UpsertQueue = LifoQueue()
    self._DeleteQueue = LifoQueue()

  async def populate_queue_of_pending_changes(
      self
  ) -> None:
    while True:
      new_notification = await self.observer.monitor_system()
      deletes = new_notification.events['delete']
      upserts = new_notification.events['upsert']
      if list(deletes.values()):
        self._DeleteQueue.put_nowait(deletes)
      if list(upserts.values()):
        self._UpsertQueue.put_nowait(upserts)

  async def consume_pending_upserts(
      self,
  ) -> AsyncGenerator[Dict[str, str], None]:
    while True:
      item = await self._UpsertQueue.get()
      if item is None:
        self._UpsertQueue.task_done()
        break
      try:
        yield item
      finally:
        self._UpsertQueue.task_done()

  async def consume_pending_deletes(
      self
  ) -> AsyncGenerator[Dict[str, str], None]:
    while True:
      item = await self._DeleteQueue.get()
      if item is None:
        self._DeleteQueue.task_done()
        break
      try:
        yield item
      finally:
        self._DeleteQueue.task_done()