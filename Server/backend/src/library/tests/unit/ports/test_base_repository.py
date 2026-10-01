from datetime import date

import pytest
from ....Infrastructure.repository.base_repository import SqliteLibraryRepository
from ....Domain.data.library import Library
from ....Domain.data.library import Book

class TestSqliteLibraryRepository:
  @pytest.fixture
  def repository(
      self
  ) -> SqliteLibraryRepository:
    uri = 'sqlite:///:memory:'
    return SqliteLibraryRepository(uri)

  @pytest.fixture
  def populated_library(
      self
  ) -> Library:
    library = Library()
    library.add_to_list_of_books(
      Book(
        title="The Devops Handbook",
        location="my downloads folder",
        file_type='.epub',
        date_added=date.fromisoformat('2001-01-01'),
      )
    )
    return library

  @pytest.fixture
  def populated_repository(
    self,
    repository: SqliteLibraryRepository,
    populated_library: Library
  ) -> SqliteLibraryRepository:
    uri = 'sqlite:///:memory:'
    sqlite_library = SqliteLibraryRepository(uri)
    sqlite_library.store_library(populated_library)
    return sqlite_library

  @pytest.fixture
  def changed_library(
    self
  ) -> Library:
    library = Library()
    library.add_to_list_of_books(
      Book(
        title="The Devops Handbook",
        location="my downloads folder",
        file_type='.epub',
        date_added=date.fromisoformat('2001-01-01'),
        date_last_accessed=date.fromisoformat('2067-04-20'),
      )
    )
    return library

  def test_check_if_storage_is_created(
      self,
      repository
  ):
    created = repository.check_if_created()
    assert created

  def test_check_if_storage_is_empty(
      self,
      repository
  ) -> bool:
    populated = repository.check_if_populated()
    assert not populated

  def test_store_library(
      self,
      repository,
      populated_library
  ):
    repository.store_library(populated_library)
    is_populated = repository.check_if_populated()

    assert is_populated

  def test_store_empty_library(
      self,
      repository
  ):
    unpopulated_library = Library()
    repository.store_library(unpopulated_library)

    is_populated = repository.check_if_populated()

    assert not is_populated

  def test_clear_repository(
      self,
      repository,
      populated_library
  ):
    repository.store_library(populated_library)
    repository.clear_library()
    is_populated = repository.check_if_populated()
    is_created = repository.check_if_created()

    assert not is_populated
    assert is_created

  def test_upsert_into_library(
    self,
    populated_repository: SqliteLibraryRepository,
    changed_library: Library
  ):
    # When
    library_of_old_books = populated_repository.get_library()
    populated_repository.upsert_book_into_library(changed_library)
    library_of_new_books = populated_repository.get_library()
    old_book = library_of_old_books.list_of_books[0]
    new_book = library_of_new_books.list_of_books[0]

    # Then
    assert old_book != new_book

  def test_get_on_empty_library(
      self,
      repository
  ):
    library_result = repository.get_library()

    assert len(library_result.list_of_books) == 0

  def test_delete_on_library(
    self,
    populated_repository: SqliteLibraryRepository,
  ):
    old_library = populated_repository.get_library()
    populated_repository.delete_books_from_library(old_library)
    new_library = populated_repository.get_library()
    assert len(new_library.list_of_books) < len(old_library.list_of_books)
    assert any(
      book not in new_library.list_of_books
      for book in old_library.list_of_books
    )