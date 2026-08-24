from backend.src.library.Domain.data.library import Library


class LibraryResultService:

  def check_if_has_book(
      self,
      library: Library
  ) -> None:

    if not library.list_of_books:
      raise ValueError(
        'No books available in designated '
        'locations, please try again'
      )