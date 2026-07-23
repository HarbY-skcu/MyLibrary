from dataclasses import dataclass, field
from books import Book
from typing import List, Iterator


@dataclass
class Library:
  list_of_books: List[Book] = field(
    default_factory = list,
    metadata = {
      "description" : "List of all books in the specified file directories"
    }
  )

  def add_to_list_of_books(
      self,
      book: Book
  ) -> None:
    self.list_of_books.append(book)

  def __iter__(self) -> Iterator[Book]:
    for book in self.list_of_books:
      yield book