from dataclasses import dataclass, field
from typing import List, Iterator, Mapping, Dict
from datetime import datetime

from backend.src.library.Infrastructure.configurator.json_configurator import JsonConfigReader


@dataclass(
  frozen = True
)
class BookNotification:
  timestamp: datetime = field(
    metadata = {
      "description" : "Time when event that caused the notification occurred"
    }
  )

  events: Dict[str, Dict[str, str]] = field(
    metadata = {
      "description" : "Dictionary of events and actions that have occurred."
                      "One dictionary for upserts, other for deletes"
    }
  )

  def __post_init__(self):
    if (
      ["upsert", "delete"] not in list(self.events.keys())
      and len(self.events.keys()) != 2
    ):
      raise ValueError(
        "Error: Notifications must only "
        "have both deletes and upserts\n"
        f"{self.events.keys()}"
      )

    if not any(
        list(dirs.values())
        for dirs in self.events.values()
    ):
      raise ValueError(
        "Notification event locations must "
        "never be empty"
      )