import asyncio

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.sse import EventSourceResponse
from typing import Annotated, AsyncIterable

from backend.src.library.Application.Features.persist_books_to_app import PersistBooksToAppFeature
from ...Application.Features.change_library_app_catalogue import ChangeLibraryCatalogueFeature
from ...Application.Features.report_changes_from_source import ReportChangesFromSourceFeature
from ...Application.Services.book_identifier_service import BookIdentifierService
from ...Domain.data.books import Book
from ...Domain.data.library import Library
from ...Domain.schemas.responses.initial_persistance import MakeAndPopulateLibraryResponse
from ...Domain.schemas.responses.library_contents import ConsolidatedLibrary, GatheredBook
from ...Domain.schemas.responses.update_events import UpdateEvent
from ...Infrastructure.configurator.base_configurator import StaticConfigReader
from ...Infrastructure.extractor.base_extractor import WindowsFileSystemExtractor
from ...Infrastructure.observer.watchdog_observer import WatchdogMonitor
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

def make_observer_feature_controller(
) -> ReportChangesFromSourceFeature:
  my_observer = WatchdogMonitor()
  return ReportChangesFromSourceFeature(
    book_observer=my_observer,
  )

def windows_file_extractor(
  my_config: StaticConfigReader,
) -> WindowsFileSystemExtractor:
  my_extractor = WindowsFileSystemExtractor()
  my_extractor.set_file_types(my_config.get_book_types())
  my_extractor.set_search_directories(my_config.get_search_directories())
  return my_extractor

def make_change_library_controller(
) -> ChangeLibraryCatalogueFeature:
  my_config = StaticConfigReader()
  uri = my_config.get_storage_location()
  my_repository = SqliteLibraryRepository(uri[0])
  my_extractor = windows_file_extractor()
  book_id_service = BookIdentifierService()
  return ChangeLibraryCatalogueFeature(
    repository=my_repository,
    extractor=my_extractor,
    book_identity_service=book_id_service,
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

@initial_persistence_router.post(
  '/Library/Updates',
  status_code = status.HTTP_200_OK,
  response_model = EventSourceResponse
)
async def report_library_updates(
  observer_feature_controller: Annotated[make_observer_feature_controller(), Depends()],
  change_library_controller: Annotated[make_change_library_controller(), Depends()],
) -> AsyncIterable[UpdateEvent]:
  observer_feature_controller.populate_queue_of_pending_changes()
  while True:
    async for notification in observer_feature_controller.consume_pending_changes():
      change_library_controller.update_library(notification)
      updated_library = change_library_controller.retrieve_updated_library()
      yield UpdateEvent(
        message = "Successfully updated library",
        changed_books = consolidate_library(updated_library)
      )

def consolidate_library(
  updated_library: Library
) -> ConsolidatedLibrary:
  gathered_books = list()
  for books in updated_library.list_of_books:
    gathered_books.append(
      GatheredBook(
        title = books.title,
        location = books.location,
        file_type = books.file_type,
        date_added = books.date_added,
        date_last_accessed = books.date_last_accessed,
        cover_image = books.cover_image,
      )
    )
    if len(gathered_books) < 1:
      raise ValueError
    return ConsolidatedLibrary(
      books = gathered_books,
    )