from datetime import date
from uuid import UUID

from sqlalchemy import (
    BigInteger, DateTime, Integer, Float, ForeignKey, String, Uuid,
    func, text
    )
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created_at: Mapped[date] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    @property
    def created_at_str(self) -> str:
        if self.created_at is None:
            return "Не указано"
        return self.created_at.strftime("%Y.%m.%d %H:%M")


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    real_first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    real_last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    class_letter: Mapped[int | None] = mapped_column(String, nullable=True)
    # created_at добавляется из Base

    def __repr__(self) -> str:
        if self.last_name is None:
            name = self.first_name
        else:
            name = f"{self.first_name} {self.last_name}"
        return f"[{self.telegram_id}] {name}"

    achevements: Mapped[list["Achevements"]] = relationship(
        back_populates="user")


class Achevements(Base):
    __tablename__ = 'achevements'

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
    )
    first_subject: Mapped[str] = mapped_column(
        String, nullable=False)
    first_subject_group: Mapped[str] = mapped_column(
        String, nullable=False)
    first_subject_group_index: Mapped[int] = mapped_column(
        Integer, nullable=False)
    first_subject_first_grade: Mapped[float] = mapped_column(
        Float,  nullable=False)
    first_subject_second_grade: Mapped[float] = mapped_column(
        Float,  nullable=False)
    first_subject_exam_grade: Mapped[int] = mapped_column(
        Integer,  nullable=False)
    second_subject: Mapped[str] = mapped_column(
        String, nullable=False)
    second_subject_group: Mapped[str] = mapped_column(
        String, nullable=False)
    second_subject_group_index: Mapped[int] = mapped_column(
        Integer, nullable=False)
    second_subject_first_grade: Mapped[float] = mapped_column(
        Float,  nullable=False)
    second_subject_second_grade: Mapped[float] = mapped_column(
        Float,  nullable=False)
    second_subject_exam_grade: Mapped[int] = mapped_column(
        Integer,  nullable=False)
    olymp: Mapped[str] = mapped_column(
        String,  nullable=False)
    olymp_grade: Mapped[int] = mapped_column(
        Integer,  nullable=False)
    year_grade: Mapped[float] = mapped_column(
        Float,  nullable=False)
    result: Mapped[float] = mapped_column(
        Float,  nullable=False)

    user: Mapped["User"] = relationship(back_populates="achevements")
