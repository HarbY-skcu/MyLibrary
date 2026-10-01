from typing import Protocol, List, AsyncGenerator, runtime_checkable

from backend.src.library.Domain.data.notification import BookNotification



class SystemMonitor(Protocol):

  def set_observed_directories(
      self,
      directories: List[str]
  ) -> None:
    ...

  def monitor_system(
      self
  ) -> AsyncGenerator[BookNotification, None]:
    ...