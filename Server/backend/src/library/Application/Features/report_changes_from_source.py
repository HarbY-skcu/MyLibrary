from typing import AsyncGenerator, Annotated

from backend.src.library.Application.ports.observer import SystemMonitor
from backend.src.library.Domain.data.notification import BookNotification
from backend.src.library.Infrastructure.observer.watchdog_observer import WatchdogMonitor

from asyncio import Queue

class ReportChangesFromSourceFeature:

  def __init__(
      self,
      book_observer: Annotated[SystemMonitor,],
  ):
    self.observer = book_observer
    self._ChangesQueue: Queue[BookNotification | None] = Queue()

  async def populate_queue_of_pending_changes(
      self
  ) -> None:
    while True:
      notification_generator = await self.observer.monitor_system()
      async for new_notification in notification_generator:
        deletes = new_notification.events['delete']
        upserts = new_notification.events['upsert']
        if list(deletes.values()) or list(upserts.values()):
          self._ChangesQueue.put_nowait(new_notification)

  async def consume_pending_changes(
      self
  ) -> AsyncGenerator[BookNotification, None]:
    while True:
      item = await self._ChangesQueue.get()
      if item is None:
        self._ChangesQueue.task_done()
        break
      try:
        yield item
      finally:
        self._ChangesQueue.task_done()