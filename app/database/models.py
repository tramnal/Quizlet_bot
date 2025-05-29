from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connect_to_db import Base


class UserWord(Base):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    word: Mapped[str] = mapped_column(String(70), index=True)
    transcription: Mapped[str] = mapped_column(String(90))
    translation: Mapped[str] = mapped_column(String(120))
    example: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str] = mapped_column(String)
