from typing import List, Dict, Any
from pathlib import Path
import json

from ...Application.ports.configurator import ConfigReader

class JsonConfigReader(ConfigReader):

  def __init__(
      self,
      config_location: Path
  ):
    self.config_location = config_location
    self.config_info: Dict[str, Any] = self._get_config_info()

  def _get_config_info(
      self
  ) -> Dict[str, Any]:
    with self.config_location.open("r") as file:
      return json.load(file)

  def get_book_types(
      self
  ) -> List[str]:
    book_types = self.config_info['book types']
    if not book_types:
      raise ValueError
    return book_types

  def get_storage_location(
      self
  ) -> str:
    db_driver = self.config_info['storage location']['driver']
    db_source_json = self.config_info['storage location']['source']
    if not db_driver or not db_source_json:
      raise ValueError("No designated storage location")
    db_source = self._convert_to_absolute_path(db_source_json)
    return db_driver + db_source


  def _convert_to_absolute_path(
      self,
      relative_path: str
  ) -> str:
    project_path = Path(__file__).parents[4]
    absolute_path = project_path / relative_path
    return str(absolute_path)

  def get_search_directories(
      self
  ) -> List[str]:
    home_path = Path(__file__).parents[8]
    directories = list()
    for directory in self.config_info['search directories']:
      directories.append(
        str(home_path / directory.replace('.', "", 1))
      )
    return directories