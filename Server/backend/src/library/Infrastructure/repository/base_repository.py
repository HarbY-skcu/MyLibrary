from sqlalchemy import engine, create_engine

from ...Application.ports.repository import LibraryRepository

from ...Domain.models.books import Books

class SqlLiteLibraryRepository(LibraryRepository):
  def __init__(
      self,
      uri: str
  ):
    self._uri = uri

  def _set_up_library(
      self
  ) -> None:
    engine = create_engine(self._uri)
