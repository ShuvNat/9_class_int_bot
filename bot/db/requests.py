from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from .models import Achevements, User


async def add_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
):

    stmt = upsert(User).values(
        {
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['telegram_id'],
        set_=dict(
            first_name=first_name,
            last_name=last_name,
        ),
    )
    await session.execute(stmt)
    await session.commit()


async def update_user(
    session: AsyncSession,
    telegram_id: int,
    real_first_name: str,
    real_last_name: str,
    class_letter: str
):
    stmt = update(User).where(
        User.telegram_id == telegram_id).values(
        real_first_name=real_first_name,
        real_last_name=real_last_name,
        class_letter=class_letter)
    await session.execute(stmt)
    await session.commit()


async def get_real_name(
    session: AsyncSession,
    telegram_id: int,
):
    stmt = select(User.real_first_name).where(
            User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    real_name = result.scalar()
    return real_name


async def save_result(
    session: AsyncSession,
    telegram_id: int,
    first_subject: str,
    first_subject_group: str,
    first_subject_group_index: int,
    first_subject_first_grade: float,
    first_subject_second_grade: float,
    first_subject_exam_grade: int,
    second_subject: str,
    second_subject_group: str,
    second_subject_group_index: int,
    second_subject_first_grade: float,
    second_subject_second_grade: float,
    second_subject_exam_grade: int,
    olymp: str,
    olymp_grade: int,
    year_grade: float,
    result: float
):
    new_result = Achevements(
        user_id=telegram_id,
        first_subject=first_subject,
        first_subject_group=first_subject_group,
        first_subject_group_index=first_subject_group_index,
        first_subject_first_grade=first_subject_first_grade,
        first_subject_second_grade=first_subject_second_grade,
        first_subject_exam_grade=first_subject_exam_grade,
        second_subject=second_subject,
        second_subject_group=second_subject_group,
        second_subject_group_index=second_subject_group_index,
        second_subject_first_grade=second_subject_first_grade,
        second_subject_second_grade=second_subject_second_grade,
        second_subject_exam_grade=second_subject_exam_grade,
        olymp=olymp,
        olymp_grade=olymp_grade,
        year_grade=year_grade,
        result=result
    )
    session.add(new_result)
    await session.flush()

    return new_result.id


async def update_result(
    session: AsyncSession,
    achevement_id: UUID,
    result: float
):
    await session.execute(
        update(Achevements)
        .where(Achevements.id == achevement_id)
        .values(result=result)
    )
    await session.commit()


async def get_results(
    session: AsyncSession
):
    stmt = (
        select(
            User.real_last_name,
            User.real_first_name,
            Achevements.first_subject,
            Achevements.first_subject_group,
            Achevements.first_subject_group_index,
            Achevements.first_subject_first_grade,
            Achevements.first_subject_second_grade,
            Achevements.first_subject_exam_grade,
            Achevements.second_subject,
            Achevements.second_subject_group,
            Achevements.second_subject_group_index,
            Achevements.second_subject_first_grade,
            Achevements.second_subject_second_grade,
            Achevements.second_subject_exam_grade,
            Achevements.olymp,
            Achevements.olymp_grade,
            Achevements.year_grade,
            Achevements.result,
            Achevements.created_at
            )
        .join(Achevements, User.telegram_id == Achevements.user_id)
        .order_by(User.last_name, User.first_name)
    )
    results = await session.execute(stmt)
    all_results = results.fetchall()
    return all_results
