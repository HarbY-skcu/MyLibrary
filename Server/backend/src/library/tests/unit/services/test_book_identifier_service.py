from pathlib import Path
from typing import Dict
from pathvalidate import is_valid_filepath

import pytest

from backend.src.library.Application.Services.book_identifier_service import BookIdentifierService
from backend.src.library.tests.fixtures.services.book_identifier_service_fixtures import BookIdentifierServiceFixtures

class TestBookIdentifierService(
  BookIdentifierServiceFixtures
):

  @pytest.mark.parametrize(
    'book_fixture',
    [
      'book_info',
      'book_with_a_period_in_name'
    ],
  )
  def test_valid_book_identified_and_parsed(
      self,
      service: BookIdentifierService,
      request,
      book_fixture: str
  ):
    book: Dict[str, str] = request.getfixturevalue(book_fixture)

    result = service.identify_book(
      book['full_name'],
      book['parent_directory']
    )

    assert not all(
      extension in result['name']
      for extension in ['.pdf', '.epub']
    )
    assert any(
      extension in result['file_type']
      for extension in ['.pdf', '.epub']
    )
    assert is_valid_filepath(Path(result['location']), platform = "auto")

  @pytest.mark.parametrize(
    'invalid_book_fixture',
    [
      'book_without_extension',
      'book_without_name',
    ]
  )
  def test_invalid_book_info_is_caught_and_raised(
      self,
      service,
      request,
      invalid_book_fixture: str
  ):
    invalid_book: Dict[str, str] = request.getfixturevalue(invalid_book_fixture)

    with pytest.raises(
        ValueError,
        match = 'Invalid book information, please try again'
    ):
      service.identify_book(
        invalid_book['full_name'],
        invalid_book['parent_directory']
      )