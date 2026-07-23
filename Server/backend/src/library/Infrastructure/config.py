from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
  db_url: str = 'sqlite:///MyLibrary.db'