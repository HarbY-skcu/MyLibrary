from datetime import date
from typing import List

from pydantic import BaseModel, Field, ConfigDict

class ConsolidatedLibrary(BaseModel):
  books: List[GatheredBook] = Field(description="List of books gathered")

class GatheredBook(BaseModel):
  title: str = Field(description= "Title of the book")
  location: str = Field(description = "File location of the book")
  file_type: str = Field(description = "File type for the book")
  date_added: date = Field(description="time file was created/added to the file system")
  date_last_accessed: date | None = Field(
    description = "date file was last opened, defaults "
                  "to creation date if it does not exist"
  )
  cover_image: int = Field(
    description = "title cover for the book; defaults to"
                  " default book cover if does not exist"
  )

  model_config = ConfigDict(
    strict=True
  )