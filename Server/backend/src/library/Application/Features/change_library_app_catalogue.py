from pathlib import Path
from typing import Dict, List
from datetime import date

from backend.src.library.Application.Services.book_identifier_service import BookIdentifierService
from backend.src.library.Application.ports.extractor import ChangedBookExtractor
from backend.src.library.Application.ports.repository import BookRepository
from backend.src.library.Domain.data.library import Library
from backend.src.library.Domain.data.books import Book


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
    upserted_books = list(
      self.extractor.extract_books_from_list(
        upserts
      )
    )
    upsert_library = Library(upserted_books)
    self.repository.upsert_book_into_library(upsert_library)

  def _delete_from_library(
      self,
      deletes: Dict[str, str]
  ):
    delete_library = Library()
    book_identifiers = self._get_book_identifiers(deletes)
    for identifier in book_identifiers:
      delete_library.add_to_list_of_books(
        self._make_book_from_identifiers(identifier)
      )
    self.repository.delete_book_from_library(delete_library)

  def _make_book_from_identifiers(
    self,
    book_identifier: Dict[str, str]
  ) -> Book:
    return Book(
      title= book_identifier['title'],
      file_type=book_identifier['file_type'],
      location = book_identifier['location'],
      date_added= date.today(),
      date_last_accessed= date.today(),
      cover_image = 0
    )

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
    updated_library = self.repository.get_library()
    return updated_library