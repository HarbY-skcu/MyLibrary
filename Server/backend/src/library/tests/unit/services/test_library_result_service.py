import pytest

from backend.src.library.Application.Services.library_results_service import LibraryResultService
from backend.src.library.Domain.data.library import Library
from backend.src.library.tests.fixtures.services.library_result_service_fixtures import LibraryResultServiceFixtures


class TestLibraryResultService(
  LibraryResultServiceFixtures
):

  def test_that_empty_library_raises_error(
      self,
      empty_library: Library,
      service: LibraryResultService
  ):
    with pytest.raises(
      ValueError,
      match='No books available in designated '
      'locations, please try again'
    ):
      service.check_if_has_book(empty_library)

  def test_that_filled_library_does_not_raise_error(
      self,
      populated_library: Library,
      service: LibraryResultService
  ):
    result = service.check_if_has_book(populated_library)

    assert result is None