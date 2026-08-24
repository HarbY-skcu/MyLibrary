from datetime import date

import pytest

from backend.src.library.Application.Features.persist_books_to_app import PersistBooksToAppFeature
from backend.src.library.Application.Services.library_results_service import LibraryResultService
from backend.src.library.Domain.data.books import Book
from backend.src.library.Domain.data.library import Library


class PersistBooksToAppFeatureFixtures:
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
  def library_result_service(
      self
  ) -> LibraryResultService:
    return LibraryResultService()

  @pytest.fixture
  def mock_feature(
      self,
      mock_reader,
      mock_repository,
      mock_config,
      library_result_service
  ):
    return PersistBooksToAppFeature(
      reader=mock_reader,
      repository=mock_repository,
      config=mock_config,
      library_result_service= library_result_service
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