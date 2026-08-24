from pathlib import Path
from typing import List

from backend.src.library.Application.ports.configurator import ConfigReader

class MockConfigurator(ConfigReader):

  def get_search_directories(
      self
  ) -> List[str]:
    return [
      "C:\\Users\\User 2\\Downloads",
      "C:\\Users\\User 1\\Downloads"
    ]

  def get_book_types(
      self
  ) -> List[str]:
    return [
      '.pdf', '.epub'
    ]

  def get_storage_location(
      self
  ) -> str:
    return f"sqlite:///{Path("./src/tests/fixtures/temp_db/temp_db.db")}"