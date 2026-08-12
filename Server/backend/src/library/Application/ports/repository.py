from typing import Protocol

from ...Domain.data.books import Book
from ...Domain.data.library import Library


class LibraryRepository(Protocol):

  def check_if_created(
      self
  ) -> bool:
    ...

  def check_if_populated(
      self
  ) -> bool:
    ...

  def clear_library(
      self
  ) -> None:
    ...

  def store_library(
      self,
      library: Library
  ) -> None:
    ...

class BookRepository(Protocol):
  def check_if_created(
      self
  ) -> bool:
    ...

  def upsert_book_into_library(
      self,
      book: Book
  ):
    ...

  def delete_book_from_library(
      self,
      title: str,
      location: str,
      file_type: str
  ) -> None:
    ...

  def get_updated_library(
      self
  ) -> Library:
    ...