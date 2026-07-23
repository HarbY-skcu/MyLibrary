from typing import Protocol, Iterator, List, Tuple
from Server.backend.src.library.Domain.data.books import Book

class BookExtractor(Protocol):
  def set_search_directories(
      self,
      file_names: List[str] | str
  ) -> None:
    ...

  def set_file_types(
      self,
      allowed_file_types: List[str] | str
  ) -> None:
    ...

  def get_invalid_directories(
      self
  ) -> Tuple[List[str], List[str]]:
    ...


  def extract_all_books(
      self
  ) -> Iterator[Book]:
    ...
