from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from ...Application.Services.persist_books_to_app import PersistBooksToAppFeature
from ...Domain.schemas.responses.initial_persistance import MakeAndPopulateLibraryResponse
from ...Infrastructure.configurator.base_configurator import StaticConfigReader
from ...Infrastructure.extractor.base_extractor import WindowsFileSystemExtractor
from ...Infrastructure.repository.base_repository import SqliteLibraryRepository

initial_persistence_router = APIRouter()

def make_feature_controller(
) -> PersistBooksToAppFeature:
  my_config = StaticConfigReader()
  uri = my_config.get_storage_location()
  return PersistBooksToAppFeature(
    reader = WindowsFileSystemExtractor(),
    repository = SqliteLibraryRepository(uri[0]),
    config = my_config
  )

@initial_persistence_router.post('/library/', status_code = status.HTTP_201_CREATED)
async def make_and_populate_library_use_case(
  feature_controller: Annotated[make_feature_controller(), Depends()],
) -> MakeAndPopulateLibraryResponse:
  try:
    my_library, invalid_dirs = feature_controller.collect_all_books()
    result_status = feature_controller.persist_all_books_to_new_library(my_library)
    return MakeAndPopulateLibraryResponse(
      success = result_status,
      message = "Successfully initialized and populated library from repository",
      empty_directories = invalid_dirs
    )
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error of the following has occurred: {str(e)}"
    )
