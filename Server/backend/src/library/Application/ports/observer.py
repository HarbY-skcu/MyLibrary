from typing import Protocol, List, AsyncGenerator, runtime_checkable

from backend.src.library.Domain.data.notification import BookNotification



class SystemObserver(Protocol):
  def set_observed_directories(
      self,
      directories: List[str]
  ) -> None:
    ...

  async def monitor_system(
      self
  ) -> AsyncGenerator[BookNotification, None]:
    ...