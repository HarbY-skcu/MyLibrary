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