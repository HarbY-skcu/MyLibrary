from ..ports.configurator import ConfigReader
from ..ports.extractor import BookExtractor
from ..ports.repository import LibraryRepository
from ...Domain.data.books import Book
from ...Domain.data.library import Library

class PersistBooksToApp:
  def __init__(
      self,
      reader: BookExtractor,
      repository: LibraryRepository,
      config: ConfigReader
  ):
    self.reader = reader
    self.repository = repository
    self.config = config

  def collect_books(
      self
  ) -> Library:
    directories = self.config.get_searched_dictionaries()
    book_types = self.config.get_book_types()
    self.reader.set_search_directories(directories)
    self.reader.set_file_types(book_types)

    my_library = Library()

    for book in self.reader.extract_all_books():
      my_library.add_to_list_of_books(book)

    return my_library

  def persist_to_new_library(
      self,
      new_library: Library
  ) -> bool:

    if not self.repository.check_if_created():
      self.repository.set_up_library()

    if self.repository.check_if_full():
      self.repository.clear_library()

    self.repository.store_library(new_library)

    return self.repository.check_if_full()