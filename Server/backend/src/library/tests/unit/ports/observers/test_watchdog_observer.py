from pathlib import Path
from typing import List

import pytest
from watchdog.observers import Observer

from backend.src.library.Infrastructure.observer.watchdog_observer import WatchdogObserver
from backend.src.library.tests.fixtures.ports.mocked_watchdog import MockedObserver, MockedEventQueue


class TestWatchdogObserver:

  def mocked_observer(
      self
  ) -> MockedObserver:
    return MockedObserver()

  @pytest.fixture
  def watchdog_observer_with_upserts(
      self,
      monkeypatch
  ):
    new_watchdog = WatchdogObserver(
      observer = MockedObserver()
    )
    return new_watchdog

  @pytest.fixture
  def fixtures_base_dir(
      self
  ) -> Path:
    return Path(__file__).resolve().parents[7]

  @pytest.fixture
  def good_directories(
      self,
      fixtures_base_dir: Path
  ) -> List[str]:
    return [
      str(
        fixtures_base_dir
        / "backend/src/library/tests/fixtures/sample data/all books"
      )
    ]

  @pytest.fixture
  def bad_directories(
      self
  ) -> List[str]:
    return [
      'does/not/exist'
    ]

  @pytest.fixture
  def mixed_directories(
      self,
      bad_directories: List[str],
      good_directories: List[str],
  ) -> List[str]:
    cpy_dir_1 = good_directories[:]
    cpy_dir_2 = bad_directories[:]
    cpy_dir_1.extend(cpy_dir_2)
    return cpy_dir_1

  def test_setting_observed_directories_with_valid_directories(
      self,
      watchdog_observer_with_upserts: WatchdogObserver,
      good_directories: List[str]
  ) -> None:
    # When
    watchdog_observer_with_upserts.set_observed_directories(
      directories=good_directories
    )

    print(good_directories)
    print(watchdog_observer_with_upserts.observed_dirs)
    # Then
    assert watchdog_observer_with_upserts.observed_dirs
    assert all(
      directory in watchdog_observer_with_upserts.observed_dirs
      for directory in good_directories
    )

  def test_setting_observed_directories_with_invalid_directories(
      self,
      watchdog_observer_with_upserts: WatchdogObserver,
      bad_directories: List[str]
  ) -> None:
    # When
    watchdog_observer_with_upserts.set_observed_directories(
      directories=bad_directories
    )

    print(bad_directories)
    print(watchdog_observer_with_upserts.observed_dirs)
    # Then
    assert all(
      fake_directory not in watchdog_observer_with_upserts.observed_dirs
      for fake_directory in bad_directories
    )

  def test_setting_observed_directories_with_valid_and_invalid_directories(
      self,
      watchdog_observer_with_upserts: WatchdogObserver,
      mixed_directories: List[str],
      good_directories: List[str],
      bad_directories: List[str]
  ) -> None:
    # When
    watchdog_observer_with_upserts.set_observed_directories(
      directories=mixed_directories
    )

    print(mixed_directories)
    print(watchdog_observer_with_upserts.observed_dirs)
    # Then
    assert watchdog_observer_with_upserts.observed_dirs
    assert all(
      directory in watchdog_observer_with_upserts.observed_dirs
      for directory in good_directories
    )
    assert all(
      fake_directory not in watchdog_observer_with_upserts.observed_dirs
      for fake_directory in bad_directories
    )

  def test_setting_observed_directories_with_no_directories(
      self,
      watchdog_observer_with_upserts: WatchdogObserver
  ) -> None:

    watchdog_observer_with_upserts.set_observed_directories(
      directories=[]
    )

    assert not watchdog_observer_with_upserts.observed_dirs

