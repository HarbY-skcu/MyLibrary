from typing import Protocol
from ...Domain.data.library import Library


class LibraryRepository(Protocol):

  def check_if_created(
      self
  ) -> bool:
    ...

  def check_if_full(
      self
  ) -> bool:
    ...

  def clear_library(
      self
  ) -> None:
    ...

  def store_library(
      self,
      library: Library
  ) -> None:
    ...