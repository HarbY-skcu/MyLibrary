from typing import List, Iterator
from pathlib import Path
from datetime import date

from ...Application.ports.extractor import BookExtractor
from ...Domain.data.library import Library
from ...Domain.data.books import Book

class WindowsFileSystemExtractor(
  BookExtractor
):

  def __init__(
      self
  ) -> None:
    self.file_types = list()
    self.directories = list()
    self.invalid_directories = list()

  def set_file_types(
      self,
      allowed_file_types: List[str] | str
  ) -> None:
    if allowed_file_types:
      self.file_types = allowed_file_types
    else:
      raise ValueError

  def set_search_directories(
      self,
      file_names: List[str] | str
  ) -> None:
    if file_names:
      self.directories = file_names
    else:
      raise ValueError

  def extract_all_books(
      self
  ) -> Iterator[Book]:
    for directory in self.directories:
      dir_path = Path(directory)
      list_of_book_locations =  self._get_book_paths(dir_path)
      if not list_of_book_locations:
        self.invalid_directories.append(directory)
        continue
      for book_locations in list_of_book_locations:
        yield self._create_book(book_locations)

  def _get_book_paths(
      self,
      directory: Path
  ) -> List[Path]:
    book_locations = list()
    for file_type in self.file_types:
      valid_files = directory.glob(f'{file_type}')
      book_locations.extend(valid_files)
    return book_locations

  @staticmethod
  def _create_book(
      system_file: Path
  ) -> Book:
    metadata = system_file.stat()
    return Book(
      title = str(system_file).split('\\')[-1].split('.')[0],
      location = str(system_file).rsplit('\\', 1)[0],
      file_type = '.' + str(system_file).rsplit('.', 1)[1],
      date_added = date.fromtimestamp(metadata.st_mtime),
      date_last_accessed = date.fromtimestamp(metadata.st_atime)
    )