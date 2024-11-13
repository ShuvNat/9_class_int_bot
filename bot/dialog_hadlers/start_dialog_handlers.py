from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests import get_real_name


async def username_getter(
        dialog_manager: DialogManager,
        event_from_user: User,
        session: AsyncSession,
        **kwargs
):
    real_name: str = await get_real_name(
        session, event_from_user.id
    )
    print(real_name)
    if real_name:
        getter_data = {
            'username': real_name,
            'first_show': False,
            'second_show': True,
            'user_id': event_from_user.id
            }
    else:
        getter_data = {
            'username': event_from_user.first_name or 'Stranger',
            'first_show': True,
            'second_show': False,
            'user_id': event_from_user.id
            }
    return getter_data
