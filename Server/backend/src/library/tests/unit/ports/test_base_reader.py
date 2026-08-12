from typing import Dict, List

import pytest
from pathlib import Path

from ....Infrastructure.extractor.base_extractor import WindowsFileSystemExtractor

class TestBaseReader:
  @pytest.fixture
  def sample_data_directories(
      self
  ) -> Dict[str, str]:
    base_path = Path(__file__).parent.resolve()
    fixtures_path = base_path.parent.parent / 'fixtures' / 'sample data'
    return {
      'valid': str(fixtures_path / 'all books'),
      'invalid': str(fixtures_path / 'no books'),
      'mixed': str(fixtures_path / 'some books'),
      'nonexistent': str(fixtures_path / 'does not exist'),
      'not a directory': str(fixtures_path / 'regular_book.pdf')
    }

  @pytest.fixture()
  def data_directories(
      self,
      request,
      sample_data_directories
  ) -> List[str]:
    return [
      sample_data_directories[key]
      for key in request.param
    ]

  @pytest.fixture
  def book_extractor(
      self
  ) -> WindowsFileSystemExtractor:
    extractor = WindowsFileSystemExtractor()
    extractor.set_file_types(
      ['.pdf', '.epub']
    )
    return extractor

  @pytest.mark.parametrize(
    "data_directories",
    [
      ['valid', 'mixed'],
      ['valid'],
      ['mixed']
    ],
    indirect = True
  )
  def test_if_all_acceptable_books_are_extracted(
      self,
      data_directories,
      book_extractor
  ):
    # Given
    book_extractor.set_search_directories(data_directories)

    # When
    books = list(book_extractor.extract_all_books())

    # Then
    assert len(books) > 0
    assert all(
      book.file_type in ['.pdf', '.epub']
      for book in books
    )

  @pytest.mark.parametrize(
    "data_directories",
    [
      ['valid', 'invalid'],
      ['mixed', 'invalid']
    ],
    indirect = True
  )
  def test_for_mixed_directories(
      self,
      data_directories,
      book_extractor
  ):

    # Given
    book_extractor.set_search_directories(data_directories)

    # When
    books = list(book_extractor.extract_all_books())

    # Then
    assert len(books) > 0
    assert len(book_extractor.empty_directories) > 0

  def test_for_empty_directory(
      self,
      sample_data_directories,
      book_extractor
  ):
    # Given
    book_extractor.set_search_directories(
      [sample_data_directories['invalid']]
    )

    # When
    books = list(book_extractor.extract_all_books())

    # Then
    assert len(books) == 0
    assert len(book_extractor.empty_directories) > 0

  @pytest.mark.parametrize(
    "data_directories",
    [
      ['nonexistent'],
      ['not a directory'],
      ['nonexistent', 'not a directory']
    ],
    indirect = True
  )
  def test_for_invalid_directory(
      self,
      data_directories,
      book_extractor
  ):
    # Given
    book_extractor.set_search_directories(
      data_directories
    )

    # When and Then
    with pytest.raises(FileNotFoundError) as err_info:
      list(book_extractor.extract_all_books())

    assert "directory does not exist" in str(err_info.value)
    assert any(
      directory in str(err_info.value)
      for directory in data_directories
    )

  def test_for_empty_file_type_configuration(
      self
  ):
    # Given
    book_extractor = WindowsFileSystemExtractor()
    empty_type_configuration = list()

    # When and Then
    with pytest.raises(ValueError, match = 'file types'):
      book_extractor.set_file_types(
        empty_type_configuration
      )

  def test_for_empty_directory_configuration(
      self,
      book_extractor: WindowsFileSystemExtractor
  ):
    # Given
    empty_directory_configuration = list()

    # When and Then
    with pytest.raises(ValueError, match = 'directories'):
      book_extractor.set_search_directories(
        empty_directory_configuration
      )