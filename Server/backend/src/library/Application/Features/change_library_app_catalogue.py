from pathlib import Path
from typing import Dict, List

from backend.src.library.Application.Services.book_identifier_service import BookIdentifierService
from backend.src.library.Application.ports.extractor import ChangedBookExtractor
from backend.src.library.Application.ports.repository import BookRepository
from backend.src.library.Domain.data.library import Library


class ChangeLibraryCatalogueFeature:

  def __init__(
      self,
      extractor: ChangedBookExtractor,
      repository: BookRepository,
      book_identity_service: BookIdentifierService
  ):
    self.extractor = extractor
    self.repository = repository
    self.book_identity_service = book_identity_service

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
    return [
      self.book_identity_service.identify_book(full_file_name, parent_directory)
      for full_file_name, parent_directory in events.items()
    ]

  def retrieve_updated_library(
      self
  ) -> Library:
    updated_library = self.repository.get_updated_library()
    return updated_library