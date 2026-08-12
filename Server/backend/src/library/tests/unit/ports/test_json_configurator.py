import pytest
from pathlib import Path

from ....Infrastructure.configurator.json_configurator import JsonConfigReader

class TestJsonConfigReader:

  @pytest.fixture
  def config_reader(
      self
  ) -> JsonConfigReader:
    config_location = Path(__file__).parents[2] / "fixtures" / "sample config" / "filled_config.json"
    return JsonConfigReader(config_location= config_location)

  def test_get_valid_book_types(
      self,
      config_reader
  ):
    # Given

    # When
    book_types = config_reader.get_book_types()

    # Then
    assert book_types
    assert all(
      book_type[0] == '.'
      for book_type in book_types
    )
    assert all(
      len(book_type) > 1
      for book_type in book_types
    )

  def test_get_book_types_when_missing(
      self
  ):
    config_location = Path(__file__).parents[2] / "fixtures" / "sample config" / "without_types.json"
    config_reader = JsonConfigReader(config_location)

    with pytest.raises(ValueError):
      config_reader.get_book_types()

  def test_get_storage_location(
      self,
      config_reader
  ):
    uri = config_reader.get_storage_location()

    assert uri

  def test_get_storage_location_when_missing(
      self
  ):
    config_location = Path(__file__).parents[2] / "fixtures" / "sample config" / "without_storage.json"
    config_reader = JsonConfigReader(config_location)

    with pytest.raises(ValueError, match = 'No designated storage location'):
      config_reader.get_storage_location()