from re import S

from dataclasses import asdict
from typing import Dict, Any, List, Sequence

from sqlalchemy import engine, create_engine, exc, inspect, Result, select, MetaData, Table, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert

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

  def upsert_book_into_library(
      self,
      upsert_library: Library
  ) -> None:
    with self.Session() as session:
      session.begin_nested()
      for upsert_book in upsert_library:
        declarative_book = self._cast_to_declarative_base(upsert_book)
        book_vars = self._get_book_vars(declarative_book)
        statement = insert(Books).values(book_vars)
        update_values_dict = self._get_update_values_dict(statement)
        update_statement = statement.on_conflict_do_update(
          index_elements = ['title', 'location', 'file_type'],
          set_ = update_values_dict
        )
        session.execute(update_statement)
      session.commit()
  
  def delete_books_from_library(
      self,
      delete_library: Library
  ) -> None:
    with self.Session() as session:
      session.begin_nested()
      for deleted_book in delete_library:
        declarative_book = self._cast_to_declarative_base(deleted_book)
        stmt = delete(Books).where(
          Books.title == declarative_book.title,
          Books.location == declarative_book.location,
          Books.file_type == declarative_book.file_type
        )
        session.execute(stmt)
      session.commit()

  @staticmethod
  def _get_update_values_dict(
    stmt
  ) -> Dict[str, Any]:
    return {
      col.name: getattr(stmt.excluded, col.name)
      for col in Books.__table__.columns
      if col.name not in ['title', 'location', 'file_type']
    }

  @staticmethod
  def _get_book_vars(
    declarative_book: Books
  ) -> Dict[str, Any]:
    return {
      col.name: getattr(declarative_book, col.name)
      for col in Books.__table__.columns
    }

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

  @staticmethod
  def _cast_to_book(
    declarative_book: Books | None
  ) -> Book | None:
    if declarative_book is None:
      return
    return Book(
      title = declarative_book.title,
      location = declarative_book.location,
      date_added = declarative_book.date_added,
      date_last_accessed = declarative_book.date_last_accessed,
      file_type = declarative_book.file_type,
      cover_image = declarative_book.cover_id
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

  def get_library(
    self
  ) -> Library:
    with self.Session() as session:
      stmt = select(Books)
      all_books = session.execute(stmt).scalars().all()
      updated_library = self._convert_to_library(all_books)
      return updated_library

  def _convert_to_library(
    self,
    list_of_books: Sequence[Books]
  ) -> Library:
    new_library = Library()
    for book in list_of_books:
      usr_book = self._cast_to_book(book)
      new_library.add_to_list_of_books(usr_book)
    return new_library