
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...Domain.models.basemodel import Base

class Covers(Base):

  __tablename__ = 'Covers'

  cover_id: Mapped[int] = mapped_column(
    ForeignKey('Books.cover_id'),
    primary_key = True,
    unique = True,
  )
  cover_location: Mapped[str] = mapped_column(
    nullable = False,
    default = 'C:\\Users\\Player 1\\Downloads\\gochiusa_april2025_syaro.jpg'
  )

  books: Mapped['Books'] = relationship(back_populates = 'covers')