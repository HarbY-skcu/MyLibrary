from pydantic import BaseModel, Field, ConfigDict

class MakeAndPopulateLibraryResponse(BaseModel):
  success: bool = Field(description = 'Success condition of initializing and populating the library')
  message: str = Field(description = 'Message describing the outcome, for logging purposes')

  model_config = ConfigDict(
    strict = True
  )