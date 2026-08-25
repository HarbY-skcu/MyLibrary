import pytest
import asyncio

from backend.src.library.Infrastructure.observer.helpers.accumulator import WatchDogEventAccumulator
from backend.src.library.tests.fixtures.ports.mocked_watchdog \
  import (
    MockedObserver,
    MockedEventQueueWithUpserts,
    MockedEventQueueWithNonBookFiles,
    MockedEventQueueWithMixedFiles
  )


class TestWatchDogEventAccumulator:

  @pytest.fixture
  def wanted_events_observer(
      self
  ) -> MockedObserver:
    return MockedObserver(
      MockedEventQueueWithUpserts()
    )

  @pytest.fixture
  def unwanted_events_observer(
      self
  ) -> MockedObserver:
    return MockedObserver(
      MockedEventQueueWithNonBookFiles()
    )

  @pytest.fixture
  def mixed_events_observer(
      self
  ) -> MockedObserver:
    return MockedObserver(
      MockedEventQueueWithMixedFiles()
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
        observer = wanted_events_observer
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
      observer=unwanted_events_observer
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
      observer=mixed_events_observer
    )

    assert list_of_observed_events
    assert all(
      Path(event.src_path).suffix in ['.pdf', '.epub']
    )
