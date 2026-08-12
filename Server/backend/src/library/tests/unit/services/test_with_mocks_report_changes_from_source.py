import asyncio
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from ....Application.Services.report_changes_from_source import ReportChangesFromSourceFeature
from ....Application.ports.observer import Observer
from ....Domain.data.notification import BookNotification


async def _never_resolves():
  await asyncio.Event().wait()

def make_feature(notification: BookNotification, mocker) -> ReportChangesFromSourceFeature:
  observer = mocker.Mock()
  observer.monitor_system = AsyncMock(side_effect=[notification, _never_resolves])
  return ReportChangesFromSourceFeature(book_observer=observer)

async def anext_or_timeout(gen, timeout: float = 1.0):
  async with asyncio.timeout(timeout):
    return await gen.__anext__()

class TestReportChangesFromSourceFeatureWithMocks:

  @pytest.fixture()
  def mock_reporter_with_both(
      self,
      mocker
  ) -> ReportChangesFromSourceFeature:
    return make_feature(
      BookNotification(
        timestamp=datetime.now(),
        events={
          'upsert': {'file 1': 'location 1'},
          'delete': {'file 2': 'location 2'},
        }
      ),
      mocker
    )

  @pytest.fixture()
  def mock_reporter_with_upserts(
      self,
      mocker
  ) -> ReportChangesFromSourceFeature:
    return make_feature(
      BookNotification(
        timestamp=datetime.now(),
        events={
          'upsert': {'file 1': 'location 1'},
          'delete': {},
        }
      ),
      mocker
    )

  @pytest.fixture()
  def mock_reporter_with_deletes(
      self,
      mocker
  ) -> ReportChangesFromSourceFeature:
    return make_feature(
      BookNotification(
        timestamp=datetime.now(),
        events={
          'upsert': {},
          'delete': {'file 2': 'location 2'},
        }
      ),
      mocker
    )

  @pytest.fixture()
  def mock_change_reporter(
      self,
      mock_observer: Observer
  ) -> ReportChangesFromSourceFeature:
    return ReportChangesFromSourceFeature(
      book_observer = mock_observer
    )

  @pytest.mark.asyncio
  async def test_populate_queue_of_pending_changes_with_upserts_and_deletes(
      self,
      mock_reporter_with_both: ReportChangesFromSourceFeature,
  ):
    populate_task = asyncio.create_task(
      mock_reporter_with_both.populate_queue_of_pending_changes()
    )

    try:
      upserted_files, deleted_files = await asyncio.gather(
        anext_or_timeout(mock_reporter_with_both.consume_pending_upserts()),
        anext_or_timeout(mock_reporter_with_both.consume_pending_deletes()),
      )
      assert upserted_files == {'file 1': 'location 1'}
      assert deleted_files == {'file 2': 'location 2'}
    finally:
      populate_task.cancel()
      await asyncio.gather(populate_task, return_exceptions=True)

  @pytest.mark.asyncio
  async def test_populate_queue_of_pending_changes_with_only_upserts(
      self,
      mock_reporter_with_upserts: ReportChangesFromSourceFeature
  ):
    populate_task = asyncio.create_task(
      mock_reporter_with_upserts.populate_queue_of_pending_changes()
    )

    try:
      upserted_files = await anext_or_timeout(mock_reporter_with_upserts.consume_pending_upserts())
      assert upserted_files == {'file 1': 'location 1'}
    finally:
      populate_task.cancel()
      await asyncio.gather(populate_task, return_exceptions=True)

  @pytest.mark.asyncio
  async def test_populate_queue_of_pending_changes_with_only_deletes(
      self,
      mock_reporter_with_deletes: ReportChangesFromSourceFeature,
  ):
    populate_task = asyncio.create_task(
      mock_reporter_with_deletes.populate_queue_of_pending_changes()
    )

    try:
      deleted_files = await anext_or_timeout(
        mock_reporter_with_deletes.consume_pending_deletes()
      )
      assert deleted_files == {'file 2': 'location 2'}
    finally:
      populate_task.cancel()
      await asyncio.gather(populate_task, return_exceptions=True)