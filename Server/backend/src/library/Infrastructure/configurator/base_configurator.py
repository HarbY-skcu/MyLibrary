from typing import List

from ...Application.ports.configurator import ConfigReader

class StaticConfigReader(ConfigReader):
  def __init__(self):
    self._list_of_book_types = list()
    self._list_of_directories = list()
    self._uri = list()
    self._set_up_vars()

  def _set_up_vars(
      self
  ) -> None:
    self._list_of_directories.append('C:\\Users\\Player 1\\Downloads')
    self._list_of_book_types.extend(('.pdf', '.epub'))
    self._uri.append('test uri')

  def get_book_types(
      self
  ) -> List[str]:
    return self._list_of_book_types

  def get_search_directories(
      self
  ) -> List[str]:
    return self._list_of_directories

  def get_storage_location(
      self
  ) -> List[str]:
    return self._uri