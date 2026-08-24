import pytest
import asyncio

from backend.src.library.Infrastructure.observer.helpers.accumulator import WatchDogEventAccumulator
from backend.src.library.tests.fixtures.ports.mocked_watchdog \
  import MockedObserver, MockedEventQueueWithUpserts, MockedEventQueueWithNonBookFiles


class TestWatchDogEventAccumulator:

  @pytest.fixture
  def wanted_events_observer(
      self
  ) -> MockedObserver:
    return MockedObserver(MockedEventQueueWithUpserts())

  @pytest.fixture
  def unwanted_events_observer(
      self
  ) -> MockedObserver:
    return MockedObserver(MockedEventQueueWithNonBookFiles())

  @pytest.fixture()
  def accumulator(
      self
  ) -> WatchDogEventAccumulator:
    return WatchDogEventAccumulator()

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
    list_of_observed_events = asyncio.create_task(
      accumulator.accumulate_events(
        observer=unwanted_events_observer
      )
    )
    await list_of_observed_events

    assert not list_of_observed_events.result()