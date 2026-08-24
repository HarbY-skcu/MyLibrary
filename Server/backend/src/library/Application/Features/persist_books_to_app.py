from typing import Tuple, List

from backend.src.library.Application.Services.library_results_service import LibraryResultService
from backend.src.library.Application.ports.configurator import ConfigReader
from backend.src.library.Application.ports.extractor import BookExtractor
from backend.src.library.Application.ports.repository import LibraryRepository
from backend.src.library.Domain.data.books import Book
from backend.src.library.Domain.data.library import Library

class PersistBooksToAppFeature:
  def __init__(
      self,
      reader: BookExtractor,
      repository: LibraryRepository,
      config: ConfigReader,
      library_result_service: LibraryResultService
  ):
    self.reader = reader
    self.repository = repository
    self.config = config
    self.library_result_service = library_result_service

  def collect_all_books(
      self
  ) -> Tuple[Library, List[str]]:
    try:
      directories = self.config.get_search_directories()
      book_types = self.config.get_book_types()
      self.reader.set_search_directories(directories)
      self.reader.set_file_types(book_types)

      my_library = Library()
      for book in self.reader.extract_all_books():
        my_library.add_to_list_of_books(book)

      self.library_result_service.check_if_has_book(my_library)

      empty_directories = self.reader.get_invalid_directories()

      return my_library, empty_directories
    except Exception as e:
      raise e

  def persist_all_books_to_new_library(
      self,
      new_library: Library
  ) -> bool:
    if not self.repository.check_if_created():
      raise FileNotFoundError("Library repository does not exist")

    if self.repository.check_if_populated():
      self.repository.clear_library()

    self.repository.store_library(new_library)

    return self.repository.check_if_populated()