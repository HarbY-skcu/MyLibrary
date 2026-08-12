from typing import List
from pydantic import BaseModel, Field, ConfigDict

class MakeAndPopulateLibraryResponse(BaseModel):
  success: bool = Field(description = 'Success condition of initializing and populating the library')
  message: str = Field(description = 'Message describing the outcome, for logging purposes')
  empty_directories: List[str] = Field(description = 'Lists all directories that contain no books to warn the user')

  model_config = ConfigDict(
    strict = True
  )