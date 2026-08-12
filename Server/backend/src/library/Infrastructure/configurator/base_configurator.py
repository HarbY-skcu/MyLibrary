from typing import List
from pathlib import Path

from ...Application.ports.configurator import ConfigReader
import Server.database as db

class StaticConfigReader(ConfigReader):
  def __init__(
      self,
      book_types: List[str] | None = None,
      directories: List[str] | None = None,
      uri: str | None = None
  ):
    self._list_of_book_types = (
      book_types
      if book_types is not None
      else ['.pdf', '.epub']
    )
    self._list_of_directories = (
      directories
      if book_types is not None
      else [str(Path.home() / 'Downloads')]
    )
    self._uri = (
      uri
      if uri is not None
      else f"sqlite:///{
        ( 
          Path(db.__file__).parent 
          / 'library.db'
        ).resolve()
      }"
    )

  def get_book_types(
      self
  ) -> List[str]:
    if not self._list_of_book_types:
      raise ValueError('No designated book types')
    return self._list_of_book_types

  def get_search_directories(
      self
  ) -> List[str]:
    return self._list_of_directories

  def get_storage_location(
      self
  ) -> str:
    if not self._uri:
      raise ValueError('No designated storage location')
    return self._uri