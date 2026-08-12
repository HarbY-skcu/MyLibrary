from typing import Protocol, List, AsyncGenerator

from backend.src.library.Domain.data.notification import BookNotification


class Observer(Protocol):
  def set_observed_directories(
      self,
      directories: List[str]
  ) -> None:
    ...

  async def monitor_system(
      self
  ) -> BookNotification:
    ...