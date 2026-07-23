from dataclasses import dataclass, field
from datetime import date

@dataclass
class Book:
  title: str = field(
    metadata = {
      "description": "Title of the book"
    }
  )
  location: str = field(
    metadata = {
      "description": "File location of the book"
    }
  )
  file_type: str = field(
    metadata = {
      "description": "File type for the book"
    }
  )
  date_added: date = field(
    metadata = {
      "description": "time file was created/added to the file system"
    }
  )
  date_last_accessed: date | None = field(
    default = None,
    metadata = {
      "description": "date file was last opened, defaults "
                     "to creation date if it does not exist"
    }
  )
  cover_image: int = field(
    default = 0,
    metadata = {
      "description": "title cover for the book; defaults to"
                     " default book cover if does not exist"
    }
  )

  def _add_default_access_date(self) -> None:
    if self.date_last_accessed is None:
      self.date_last_accessed = self.date_added

  def __post_init__(self):
    self._add_default_access_date()

    if self.file_type not in ['pdf', 'epub']:
      raise ValueError("Book file type must be 'epub' or 'pdf'")