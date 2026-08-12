from typing import Protocol, Iterator, List, Tuple, Dict
from Server.backend.src.library.Domain.data.books import Book

class BookExtractor(Protocol):
  def set_search_directories(
      self,
      file_names: List[str]
  ) -> None:
    ...

  def set_file_types(
      self,
      allowed_file_types: List[str]
  ) -> None:
    ...

  def get_invalid_directories(
      self
  ) -> List[str]:
    ...

  def extract_all_books(
      self
  ) -> Iterator[Book]:
    ...


class ChangedBookExtractor(Protocol):
  def set_search_directories(
      self,
      file_names: List[str]
  ) -> None:
    ...

  def set_file_types(
      self,
      allowed_file_types: List[str]
  ) -> None:
    ...

  def extract_books_from_list(
      self,
      book_ids = List[Dict[str, str]]
  ) -> Iterator[Book]:
    ...
