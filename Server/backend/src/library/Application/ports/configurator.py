from typing import Protocol, List, runtime_checkable

@runtime_checkable
class ConfigReader(Protocol):
  def get_search_directories(
      self
  ) -> List[str]:
    ...

  def get_book_types(
      self
  ) -> List[str]:
    ...

  def get_storage_location(
      self
  ) -> str:
    ...