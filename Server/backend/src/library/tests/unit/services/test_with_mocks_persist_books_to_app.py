from typing import List

import pytest
from datetime import date

from ....Application.Services.persist_books_to_app import PersistBooksToAppFeature
from ....Domain.data.books import Book
from ....Domain.data.library import Library


class TestPersistBooksToAppFeatureWithMocks:

  @pytest.fixture
  def mock_reader(self, mocker):
    return mocker.Mock()

  @pytest.fixture
  def mock_repository(self, mocker):
    return mocker.Mock()

  @pytest.fixture(autouse = True)
  def mock_config(self, mocker, monkeypatch):
    mock = mocker.patch(
      'Server.backend.src.library.Domain.data.books.StaticConfigReader'
    )
    mock.return_value.get_book_types.return_value = [
      '.pdf',
      '.epub'
    ]
    return mock

  @pytest.fixture
  def mock_service(self, mock_reader, mock_repository, mock_config):
    return PersistBooksToAppFeature(
      reader=mock_reader,
      repository=mock_repository,
      config=mock_config,
    )

  @pytest.fixture
  def mocked_library(self):
    my_library = Library()
    my_library.add_to_list_of_books(
      Book(
        title="The Circle of Life",
        location='test location',
        file_type='.pdf',
        date_added=date.fromisoformat('2002-02-02'),
      )
    )
    return my_library

  def test_collect_all_books_from_populated_files(
    self,
    mock_reader,
    mock_config,
    mock_service
  ):
    # given

    dir1 = "C:\\Users\\User 1\\Downloads"
    dir2 = "C:\\Users\\User 2\\Downloads"
    mock_config.get_searched_directories.return_value = [
      dir1, dir2,
    ]
    mock_config.get_book_types.return_value = [
      '.pdf', '.epub',
    ]

    book1 = Book(
        title = "The Circle of Life",
        location = dir1,
        file_type = '.pdf',
        date_added = date.fromisoformat('2002-02-02'),
    )
    book2 = Book(
        title ="The Devops Handbook",
        location = dir2,
        file_type = '.epub',
        date_added = date.fromisoformat('2001-01-01'),
    )
    mock_reader.extract_all_books.return_value = (
      iter([book1, book2])
    )
    # When
    library, _ = mock_service.collect_all_books()

    # Then
    assert len(library.list_of_books) == 2
    assert (book1 in library.list_of_books and
            book2 in library.list_of_books)


  def test_if_collected_invalid_directory_raises_warning(
      self,
      mock_config,
      mock_reader,
      mock_service
  ):
    # Given
    dir1 = "C:\\Users\\User 1\\Downloads"
    dir2 = "C:\\Users\\User 2\\Non-existent Folder"
    mock_config.get_searched_directories.return_value = [
      dir1, dir2,
    ]

    mock_reader.extract_all_books.side_effect = FileNotFoundError(
      f"Directory does not exist, please change "
      f"the configuration: {dir2}"
    )

    # When and Then
    with pytest.raises(FileNotFoundError) as err_info:
      mock_service.collect_all_books()

    assert dir2 in str(err_info.value)
    assert dir1 not in str(err_info.value)

  def test_if_no_books_are_collected(
      self,
      mock_config,
      mock_reader,
      mock_service
  ):
    # Given
    dir1 = "C:\\Users\\User 1\\Downloads"
    dir2 = "C:\\Users\\User 2\\Downloads"
    mock_config.get_searched_directories.return_value = [
      dir1, dir2,
    ]
    mock_config.get_book_types.return_value = [
      '.pdf', '.epub',
    ]

    mock_reader.extract_all_books.return_value = list()

    # When and Then
    with pytest.raises(ValueError,
      match = 'No books available in designated '
      'locations, please try again'
    ):
      mock_service.collect_all_books()

  def test_persist_all_books_to_library(
      self,
      mock_repository,
      mock_service,
      mocked_library
  ):
    # Given
    mock_repository.check_if_created.return_value = True
    mock_repository.check_if_full.side_effect = (False, True)
    mock_repository.store_library.return_value = None

    # When
    result = mock_service.persist_all_books_to_new_library(mocked_library)

    # Then
    assert result is True

  def test_if_no_place_to_persist_library(
      self,
      mock_repository,
      mock_service,
      mocked_library
  ):
    mock_repository.check_if_created.return_value = False

    with pytest.raises(
        FileNotFoundError,
        match = 'Library repository does not exist'
    ):
      mock_service.persist_all_books_to_new_library(mocked_library)
