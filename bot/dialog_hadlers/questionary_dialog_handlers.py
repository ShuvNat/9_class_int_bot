
import re
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests import get_real_name, save_result, update_user, update_result
from .admin_dialog_handlers import (
    Classes, BASIC, EXAM_BASIC, EXAM_PRO, MAX, OLYMP, PRO
    )


def is_valid_number(text):
    return bool(
        re.match(r"^(?:[1-4](?:[.,]\d{1,2})?|5(?:[.,]0{1,2})?)$", text)
        )


async def first_name_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager):
    if message.text.isalpha():
        dialog_manager.dialog_data["first_name"] = message.text
        await dialog_manager.next()
    else:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(text='Пожалуйста, напишите только имя')


async def last_name_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager):
    if message.text.isalpha():
        dialog_manager.dialog_data["last_name"] = message.text
        await dialog_manager.next()
    else:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(text='Пожалуйста, напишите только фамилию')


async def class_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    classes = [[name, value] for name, value in Classes.__dict__.items()
               if not name.startswith("__")]
    return {'classes': classes}


async def class_handler(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    selected_item: str,
):
    classes = Classes()
    current_class = getattr(classes, selected_item)
    dialog_manager.dialog_data['class'] = current_class
    session = dialog_manager.middleware_data['session']
    await update_user(session, callback.from_user.id,
                      *dialog_manager.dialog_data.values())
    dialog_manager.dialog_data.clear()
    await dialog_manager.next()


async def subject_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    subjects = [
        ['Математика'],
        ['Физика'],
        ['Информатика'],
        ['Литература'],
        ['История'],
        ['Oбществознание'],
        ['Химия'],
        ['Биология']
    ]
    return {'subjects': subjects}


async def select_handler(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    selected_item: str,
):
    if (widget.widget_id == 'second_subject' and
       dialog_manager.dialog_data['first_subject'] == selected_item):
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await callback.message.answer(
            text='Вы уже выбрали этот предмет, как первый, '
                 'пожалуйста, выберите другой\n'
                 )
        return
    dialog_manager.dialog_data[f'{widget.widget_id}'] = selected_item
    await dialog_manager.next()


async def group_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    groups = [
        ['Базовая',],
        ['Средняя', ],
        ['Углубленная',]
    ]
    return {'groups': groups}


async def grade_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    if 'grades' not in dialog_manager.dialog_data:
        dialog_manager.dialog_data['grades'] = []
    if is_valid_number(message.text):
        grade = float(message.text.replace(",", "."))
        dialog_manager.dialog_data.get('grades').append(grade)
        await dialog_manager.next()
    else:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(
            text='Пожалуйста, напишите число от 1 до 5 с точностью до сотых\n'
                 )


async def exam_grade_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    if 'exam_grades' not in dialog_manager.dialog_data:
        dialog_manager.dialog_data['exam_grades'] = []
    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        dialog_manager.dialog_data.get('exam_grades').append(int(message.text))
        await dialog_manager.next()
    else:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(
            text='Пожалуйста, напишите целое число от 1 до 10\n'
                 )


async def olymp_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    olymp = [
        ['Нет'],
        ['Муниципальный тур'],
        ['Региональный тур'],
        ['Финал']
    ]
    return {'olymp': olymp}


async def result_getter(
    dialog_manager: DialogManager,
    event_from_user: User,
    session: AsyncSession,
    **kwargs
):

    fs = dialog_manager.dialog_data['first_subject']
    fsg = dialog_manager.dialog_data['first_subject_group']
    fsfg = dialog_manager.dialog_data['grades'][0]
    fssg = dialog_manager.dialog_data['grades'][1]
    fseg = dialog_manager.dialog_data['exam_grades'][0]
    ss = dialog_manager.dialog_data['second_subject']
    ssg = dialog_manager.dialog_data['second_subject_group']
    ssfg = dialog_manager.dialog_data['grades'][2]
    sssg = dialog_manager.dialog_data['grades'][3]
    sseg = dialog_manager.dialog_data['exam_grades'][1]
    olymp = dialog_manager.dialog_data['olymp']
    year = dialog_manager.dialog_data['grades'][4]
    result = 0

    if fsg == 'Базовая':
        fsgi = 0
    else:
        fsgi = 1

    if ssg == 'Базовая':
        ssgi = 0
    else:
        ssgi = 1

    if olymp == 'Het':
        olymp_grade = 0
    elif olymp == 'Муниципальный тур':
        olymp_grade = 2
    elif olymp == 'Региональный тур':
        olymp_grade = 7
    else:
        olymp_grade = 10

    achevement_id = await save_result(
        session, event_from_user.id, fs, fsg, fsgi, fsfg, fssg, fseg,
        ss, ssg, ssgi, ssfg, sssg, sseg, olymp, olymp_grade, year, result
        )

    if fsgi == 1:
        fsfg *= PRO.value
        fssg *= PRO.value
        fseg *= EXAM_PRO.value
    if ssgi == 1:
        ssfg *= PRO.value
        sssg *= PRO.value
        sseg *= EXAM_PRO.value

    calculate = ((fsfg + fssg + ssfg + sssg + year) * BASIC.value +
                 (fseg + sseg) * EXAM_BASIC.value +
                 olymp_grade*OLYMP.value - 5)/MAX.value*100

    result = round(calculate, 2)

    await update_result(session, achevement_id, result)

    real_name = await get_real_name(session, event_from_user.id)
    if result <= 40:
        text = 1
    elif result <= 50:
        text = 2
    elif result <= 60:
        text = 3
    elif result <= 70:
        text = 4
    else:
        text = 5
    return {'text': text,
            'result': result,
            'real_name': real_name}
