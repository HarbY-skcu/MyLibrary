import queue
from pathlib import Path

import pytest
import asyncio

from backend.src.library.Infrastructure.observer.helpers.accumulator import WatchDogEventAccumulator
from backend.src.library.tests.fixtures.ports.mocked_watchdog \
  import (
    MockedObserver,
    mocked_event_queue_with_deletes,
    mocked_event_queue_with_mixed_files,
    mocked_event_queue_with_upsets,
    mocked_event_queue_with_unwanted_files,
    mixed_file_type_events,
    events_with_non_book_files,
    upsert_events
  )


class TestWatchDogEventAccumulator:

  @pytest.fixture
  def wanted_events_observer(
    self,
    mocked_event_queue_with_upsets: queue.Queue
  ) -> MockedObserver:
    return MockedObserver(
      mocked_event_queue_with_upsets
    )

  @pytest.fixture
  def unwanted_events_observer(
    self,
    mocked_event_queue_with_unwanted_files: queue.Queue
  ) -> MockedObserver:
    return MockedObserver(
      mocked_event_queue_with_unwanted_files
    )

  @pytest.fixture
  def mixed_events_observer(
    self,
    mocked_event_queue_with_mixed_files: queue.Queue
  ) -> MockedObserver:
    return MockedObserver(
      mocked_event_queue_with_mixed_files
    )

  @pytest.fixture()
  def accumulator(
    self
  ) -> WatchDogEventAccumulator:
    return WatchDogEventAccumulator(first_event_timeout=.5)

  @pytest.mark.asyncio
  async def test_that_events_are_accumulated(
    self,
    wanted_events_observer: MockedObserver,
    accumulator: WatchDogEventAccumulator
  ) -> None:
    # When
    list_of_observed_events = asyncio.create_task(
      accumulator.accumulate_events(
        event_queue = wanted_events_observer.event_queue
      )
    )
    await list_of_observed_events

    # Then
    assert list_of_observed_events.result()

  @pytest.mark.asyncio
  async def test_that_events_are_excluded_for_files_that_are_not_books(
    self,
    unwanted_events_observer: MockedObserver,
    accumulator: WatchDogEventAccumulator
  ) -> None:
    # When
    list_of_observed_events = await accumulator.accumulate_events(
      event_queue=unwanted_events_observer.event_queue
    )

    # Then
    assert list_of_observed_events == []

  @pytest.mark.asyncio
  async def test_that_events_are_separated_from_relevant_and_irrelevant_files(
    self,
    mixed_events_observer: MockedObserver,
    accumulator: WatchDogEventAccumulator
  ):
    list_of_observed_events = await accumulator.accumulate_events(
      event_queue=mixed_events_observer.event_queue
    )

    assert list_of_observed_events
    assert all(
      Path(str(event.src_path)).suffix in ['.pdf', '.epub']
      for event in list_of_observed_events
    )
