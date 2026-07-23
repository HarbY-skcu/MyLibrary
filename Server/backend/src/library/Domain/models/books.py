from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from .covers import Covers
from ...Domain.models.basemodel import Base

class Books(Base):

  __tablename__ = 'Books'

  title: Mapped[str] = mapped_column(
    primary_key = True
  ) # used as a foreign key for tags and descriptions
  location: Mapped[str] = mapped_column(
    primary_key = True
  )
  file_type: Mapped[str] = mapped_column(
    primary_key = True,
    nullable = False
  )
  date_added: Mapped[date] = mapped_column(
    nullable = False
  )
  date_last_accessed: Mapped[date] = mapped_column(
    nullable = False
  )
  cover_id: Mapped[int] = mapped_column(
    nullable = False
  ) # foreign key related to the cover page

  covers: Mapped['Covers'] = relationship(back_populates = 'covers')