from typing import Dict

import pytest

from backend.src.library.Application.Services.book_identifier_service import BookIdentifierService


class BookIdentifierServiceFixtures:

  @pytest.fixture
  def book_without_extension(
      self
  ) -> Dict[str, str]:
    return {
      'full_name' : 'book-title',
      'parent_directory' : 'C:\\users\\User 1\\Downloads'
    }

  @pytest.fixture
  def book_info(
      self
  ) -> Dict[str, str]:
    return {
      'full_name' : 'book-title.pdf',
      'parent_directory' : 'C:\\users\\User 1\\Downloads'
    }

  @pytest.fixture
  def book_without_name(
      self
  ) -> Dict[str, str]:
    return {
      'full_name' : '.pdf',
      'parent_directory' : 'C:\\users\\User 1\\Downloads'
    }

  @pytest.fixture
  def book_with_a_period_in_name(
      self
  ) -> Dict[str, str]:
    return {
      'full_name' : 'the history of .NET.pdf',
      'parent_directory' : 'C:\\users\\User 1\\Downloads'
    }

  @pytest.fixture
  def service(
      self
  ) -> BookIdentifierService:
    return BookIdentifierService()