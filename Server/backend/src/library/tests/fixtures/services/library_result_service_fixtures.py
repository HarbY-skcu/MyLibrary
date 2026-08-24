from datetime import date

import pytest

from backend.src.library.Application.Services.library_results_service import LibraryResultService
from backend.src.library.Domain.data.books import Book
from backend.src.library.Domain.data.library import Library


class LibraryResultServiceFixtures:

  @pytest.fixture
  def empty_library(
      self
  ) -> Library:
    return Library()

  @pytest.fixture
  def book(
      self
  ) -> Book:
    return Book(
      title = "The Devops Handbook",
      location = "my downloads folder",
      file_type = '.epub',
      date_added = date.fromisoformat('2001-01-01'),
    )

  @pytest.fixture
  def populated_library(
      self,
      book: Book
  ) -> Library:
    library = Library()
    library.add_to_list_of_books(book)
    return library

  @pytest.fixture
  def service(
      self
  ) -> LibraryResultService:
    return LibraryResultService()