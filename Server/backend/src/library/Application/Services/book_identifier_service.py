from pathlib import Path
from typing import Dict


class BookIdentifierService:

  def identify_book(
      self,
      full_name: str,
      location: str
  ) -> Dict[str, str]:
    split_names = full_name.rsplit('.', 1)
    if len(split_names) == 2 and location and split_names[0]:
      name, file_type = split_names
    else:
      raise ValueError('Invalid book information, please try again:\n'
                       f'full name: {full_name}\nlocation: {location}')
    return (
      {
        'name': name,
        'file_type': '.' + file_type,
        'location': location
      }
    )