from pydantic import BaseModel, Field, ConfigDict

from backend.src.library.Domain.schemas.responses.library_contents import ConsolidatedLibrary


class UpdateEvent(BaseModel):
  message: str = Field(
    description = "Describes the occurrence of the events, "
                  "and what happened during the run.",
    default="Books have changed on native system"
  )
  changed_books: ConsolidatedLibrary = Field(
    description="Library collection of changed books"
  )