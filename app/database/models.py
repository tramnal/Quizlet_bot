from sqlalchemy import BigInteger, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserWord(Base):
    '''The main table that stores all user-submitted words'''
    __tablename__ = "user_words"
    __table_args__ = (Index('idx_user_word', 'tg_id', 'word'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    word: Mapped[str] = mapped_column(String(70), index=True)
    transcription: Mapped[str] = mapped_column(String(90))
    translation: Mapped[str] = mapped_column(String(120))
    example: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str] = mapped_column(String(255))
