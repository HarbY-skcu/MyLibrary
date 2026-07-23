import pytest

from Server.backend.src.library.Application.Services.persist_books_to_app import PersistBooksToApp
from Server.backend.src.library.Application.ports.configurator import ConfigReader
from Server.backend.src.library.Application.ports.extractor import BookExtractor
from Server.backend.src.library.Application.ports.repository import LibraryRepository


def test_collect_books():
  PersistBooksToApp(BookExtractor(), LibraryRepository(), ConfigReader())