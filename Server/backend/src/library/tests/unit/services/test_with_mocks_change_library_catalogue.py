from datetime import date
from typing import List

import pytest

from backend.src.library.Application.Services.change_library_app_catalogue import ChangeLibraryCatalogueFeature
from backend.src.library.Application.ports.extractor import ChangedBookExtractor
from backend.src.library.Application.ports.repository import BookRepository
from backend.src.library.Domain.data.books import Book
from backend.src.library.Domain.data.library import Library


class TestChangeLibraryCatalogueFeatureWithMocks:

  @pytest.fixture
  def book_extractor(
      self,
      mocker,
      list_of_new_books
  ) -> ChangedBookExtractor:
    new_mock = mocker.Mock()
    new_mock.extract_books_from_list.return_value = list_of_new_books
    return new_mock

  @pytest.fixture
  def list_of_new_books(
      self
  ) -> List[Book]:
    book1 = Book(
      title="The Circle of Life",
      location="C:\\Users\\User 1\\Downloads",
      file_type='.pdf',
      date_added=date.fromisoformat('2002-02-02'),
    )
    book2 = Book(
      title="The Devops Handbook",
      location="C:\\Users\\User 2\\Downloads",
      file_type='.epub',
      date_added=date.fromisoformat('2001-01-01'),
    )
    return [book1, book2]

  @pytest.fixture
  def list_of_deleted_books(
      self
  ) -> List[Book]:
    book3 = Book(
      title = "The Gaijin Yokozuna: the biography of Chad Rowan",
      location = "C:\\Users\\User 1\\Downloads",
      file_type = '.pdf',
      date_added = date.fromisoformat('2004-04-04')
    )
    return [book3]

  @pytest.fixture
  def upserted_library(
      self,
      list_of_new_books: List[Book]
  ) -> Library:
    return Library(
      list_of_books = list_of_new_books
    )

  @pytest.fixture
  def emptied_library(
      self
  ) -> Library:
    return Library()

  @pytest.fixture
  def filled_book_repository(
      self,
      upserted_library: Library,
      mocker
  ) -> BookRepository:
    mock = mocker.Mock()
    mock.get_updated_library.return_value = upserted_library
    mock.check_if_created.return_value = True
    return mock

  @pytest.fixture
  def empty_book_repository(
      self,
      emptied_library: Library,
      mocker
  ) -> BookRepository:
    mock = mocker.Mock()
    mock.get_updated_library.return_value = emptied_library
    mock.check_if_created.return_value = True
    return mock

  def test_that_books_are_upserted_into_repository(
      self,
      filled_book_repository: BookRepository,
      book_extractor: ChangedBookExtractor,
      list_of_new_books: List[Book]
  ):
    files_to_be_upserted = {
      "The Circle of Life.pdf": "C:\\Users\\User 1\\Downloads",
      "The Devops Handbook.epub": "C:\\Users\\User 2\\Downloads"
    }

    change_controller = ChangeLibraryCatalogueFeature(
      extractor = book_extractor,
      repository = filled_book_repository
    )
    change_controller.update_library(
      upserts = files_to_be_upserted
    )
    changed_library = change_controller.retrieve_updated_library()

    assert all(
      book in changed_library.list_of_books
      for book in list_of_new_books
    )

  def test_that_books_are_deleted_from_repository(
      self,
      empty_book_repository: BookRepository,
      book_extractor: ChangedBookExtractor,
      list_of_new_books: List[Book]
  ):
    files_to_be_deleted = {
      "The Circle of Life.pdf": "C:\\Users\\User 1\\Downloads",
      "The Devops Handbook.epub": "C:\\Users\\User 2\\Downloads"
    }

    change_controller = ChangeLibraryCatalogueFeature(
      extractor=book_extractor,
      repository=empty_book_repository
    )

    change_controller.update_library(
      upserts = files_to_be_deleted
    )
    changed_library = change_controller.retrieve_updated_library()

    assert all(
      book not in changed_library.list_of_books
      for book in list_of_new_books
    )

  def test_that_books_are_upserted_and_deleted_from_repository(
    self,
    filled_book_repository: BookRepository,
    book_extractor: ChangedBookExtractor,
    list_of_new_books: List[Book],
    list_of_deleted_books: List[Book]
  ):
    files_to_be_upserted = {
      "The Circle of Life.pdf": "C:\\Users\\User 1\\Downloads",
      "The Devops Handbook.epub": "C:\\Users\\User 2\\Downloads"
    }
    files_to_be_deleted = {
      "The Gaijin Yokozuna: "
      "the biography of Chad Rowan.pdf": "C:\\Users\\User 1\\Downloads"
    }

    change_controller = ChangeLibraryCatalogueFeature(
      extractor=book_extractor,
      repository=filled_book_repository
    )
    change_controller.update_library(
      upserts = files_to_be_upserted,
      deletes = files_to_be_deleted
    )
    changed_library = change_controller.retrieve_updated_library()

    assert all(
      book not in changed_library.list_of_books
      for book in list_of_deleted_books
    )
    assert all(
      book in changed_library.list_of_books
      for book in list_of_new_books
    )