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
      upsert_library: Library
  ) -> None:
    ...

  def delete_books_from_library(
      self,
      delete_library: Library
  ) -> None:
    ...

  def get_library(
      self
  ) -> Library:
    ...