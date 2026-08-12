from pathlib import Path
from typing import Dict, List

from ..ports.extractor import ChangedBookExtractor
from ..ports.repository import BookRepository
from ...Domain.data.library import Library


class ChangeLibraryCatalogueFeature:

  def __init__(
      self,
      extractor: ChangedBookExtractor,
      repository: BookRepository
  ):
    self.extractor = extractor
    self.repository = repository

  def update_library(
      self,
      upserts: Dict[str, str] = None,
      deletes: Dict[str, str] = None
  ) -> None:
    if not self.repository.check_if_created():
      raise ValueError("Error: Invalid operation. Database not create yet")
    if upserts:
      self._upsert_into_library(upserts)
    if deletes:
      self._delete_from_library(deletes)

  def _upsert_into_library(
      self,
      upserts: Dict[str, str]
  ):
    book_identifiers = self._get_book_identifiers(upserts)
    upserted_books = list(
      self.extractor.extract_books_from_list(
        book_identifiers
      )
    )
    for book in upserted_books:
      self.repository.upsert_book_into_library(book)

  def _delete_from_library(
      self,
      deletes: Dict[str, str]
  ):
    book_identifiers = self._get_book_identifiers(deletes)
    for info in book_identifiers:
      self.repository.delete_book_from_library(**info)

  def _get_book_identifiers(
      self,
      events: Dict[str, str]
  ) -> List[Dict[str, str]]:
    book_identifiers = list()
    for full_file_name, parent_directory in events.items():
      name, file_type = full_file_name.rsplit('.', 1)
      location = str(Path(parent_directory))
      book_identifiers.append(
        {
          'name': name,
          'file_type': '.' + file_type,
          'location': location
        }
      )
    return book_identifiers

  def retrieve_updated_library(
      self
  ) -> Library:
    updated_library = self.repository.get_updated_library()
    return updated_library