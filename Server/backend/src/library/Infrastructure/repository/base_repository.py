from sqlalchemy import engine, create_engine, exc, inspect
from sqlalchemy.orm import sessionmaker

from ...Application.ports.repository import LibraryRepository

from ...Domain.data.library import Library
from ...Domain.data.books import Book
from ...Domain.models.books import Books
from ...Domain.models.basemodel import Base

class SqliteLibraryRepository(LibraryRepository):
  def __init__(
      self,
      uri: str
  ):
    self._uri = uri
    self._set_up_library()

  def _set_up_library(
      self
  ) -> None:
    self.engine = create_engine(self._uri)
    self.Session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(self.engine)

  def store_library(
      self,
      library: Library
  ) -> None:
    with self.Session() as session:
      session.begin_nested()
      for library_book in library:
        declarative_book = self._cast_to_declarative_base(library_book)
        session.add(declarative_book)
      session.commit()

  @staticmethod
  def _cast_to_declarative_base(
      book: Book
  ) -> Books:
    return Books(
      title = book.title,
      location = book.location,
      date_added = book.date_added,
      date_last_accessed = book.date_last_accessed,
      file_type = book.file_type,
      cover_id = book.cover_image
    )

  def clear_library(
      self
  ) -> None:
    with self.Session() as session:
      session.query(Books).delete()
      session.commit()

  def check_if_populated(
      self
  ) -> bool:
    with self.Session() as session:
      if session.query(Books).first() is None:
        return False
      else:
        return True

  def check_if_created(
      self
  ) -> bool:
    inspector = inspect(self.engine)
    if inspector.has_table(Books.__tablename__):
      return True
    else:
      return False