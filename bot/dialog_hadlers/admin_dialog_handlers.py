import re
from aiogram.types import CallbackQuery, Message, FSInputFile, User
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from dataclasses import dataclass
from pandas import DataFrame, ExcelWriter
from pathlib import Path


from db.requests import get_results
from fsm.fsm_dialogs import AdminState

FILEPATH = Path(__file__).resolve().parent.parent


class Classes:
    first_class = '9Б'
    second_class = '9Г'


@dataclass
class Coefficients:
    name: str
    value: float


BASIC = Coefficients(
    'Базовый',
    0.4
)

EXAM_BASIC = Coefficients(
    'Базовый для экзаменов',
    0.9
)


PRO = Coefficients(
    'Для углубления',
    1.5
)

EXAM_PRO = Coefficients(
    'Углубление для экзаменов',
    0.9
)

OLYMP = Coefficients(
    'Олимпиадный',
    0.2
)

MAX = Coefficients(
    'Максимальная сумма баллов',
    29
)

COEFFICIENTS_LIST = [BASIC, EXAM_BASIC, EXAM_PRO, PRO, OLYMP, MAX]


def is_valid_class(text: str) -> bool:
    return bool(re.fullmatch(r"9[А-Я]", text))


def is_valid_coef(text):
    return bool(re.fullmatch(r"[0-9.,]+", text))


async def user_getter(
        dialog_manager: DialogManager,
        event_from_user: User,
        **kwargs
):
    return {'user_id': event_from_user.id}


async def get_xlsx_file(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    session = dialog_manager.middleware_data.get('session')
    list = await get_results(session)
    filename = ('Статистика.xlsx')
    filepath = FILEPATH / f'files/{filename}'
    df = DataFrame(list, columns=[
        'Фамилия',
        'Имя',
        '1 профиль',
        'Группа',
        'Коэф. группы',
        '1 полугодие',
        '2 полугодие',
        'Экзамен',
        '2 профиль',
        'Группа',
        'Коэф. группы',
        '1 полугодие',
        '2 полугодие',
        'Экзамен',
        'Олимпиада',
        'Балл олимпиады',
        'Годовой балл',
        'Результат'
        ])
    df.to_excel(filepath, index=False)
    with ExcelWriter(
            filepath, engine='openpyxl', mode='a'
            ) as writer:
        worksheet = writer.sheets['Sheet1']
        worksheet.title = 'Лист1'

        for column_cells in worksheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            worksheet.column_dimensions[
                column_cells[0].column_letter].width = length + 2
    await callback.message.answer_document(
                FSInputFile(filepath, filename=filename)
            )
    filepath.unlink()
    await dialog_manager.switch_to(
        AdminState.start,
        show_mode=ShowMode.SEND,
    )


async def class_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    classes = [[name, value] for name, value in Classes.__dict__.items()
               if not name.startswith("__")]
    return {'classes': classes}


async def select_handler(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    selected_item: str,
):
    dialog_manager.dialog_data[f'{widget.widget_id}'] = selected_item
    await dialog_manager.next()


async def class_name_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    classes_letter = dialog_manager.dialog_data['class_letter']
    class_name = getattr(Classes, classes_letter)
    return {'class_name': class_name}


async def class_rename_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    class_letter = dialog_manager.dialog_data['class_letter']
    values = [
        getattr(Classes, attr) for attr in
        dir(Classes) if not attr.startswith("__")
        ]
    if message.text in values:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(
            text='Такой класс уже существует, пожалуйста, '
            'выберите другую букву'
                 )
        return
    if is_valid_class(message.text):
        setattr(Classes, class_letter, message.text)
        dialog_manager.dialog_data['complete'] = (
            f'Спасибо, класс успешно переименован.\n'
            f'Новое название класса {message.text}'
            )

        await dialog_manager.switch_to(AdminState.complete)
    else:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(
            text='Пожалуйста, напишите название в формате 9А'
                 )


async def class_add_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    pass
    if not hasattr(Classes, 'first_class'):
        class_letter = 'first_class'
    elif not hasattr(Classes, 'second_class'):
        class_letter = 'second_class'
    elif not hasattr(Classes, 'third_class'):
        class_letter = 'third_class'
    elif not hasattr(Classes, 'forth_class'):
        class_letter = 'forth_class'
    else:
        class_letter = 'fith_class'
    values = [
        getattr(Classes, attr) for attr in
        dir(Classes) if not attr.startswith("__")
        ]
    if message.text in values:
        print(message.text)
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(
            text='Такой класс уже существует, пожалуйста, '
            'выберите другую букву'
                 )
        return
    if is_valid_class(message.text):
        print(message.text)
        setattr(Classes, class_letter, message.text)
        dialog_manager.dialog_data['complete'] = (
            f'Спасибо, класс успешно создан.\n'
            f'Название нового класса {message.text}'
        )
        await dialog_manager.switch_to(AdminState.complete)
    else:
        print(message.text)
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(
            text='Пожалуйста, напишите название в формате 9А'
                 )


async def class_delete_handler(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    classes_letter = dialog_manager.dialog_data['class_letter']
    class_name = getattr(Classes, classes_letter)
    try:
        delattr(Classes, classes_letter)
        dialog_manager.dialog_data['complete'] = (
            f'Спасибо, {class_name} класс успешно удален.\n'
        )
        await dialog_manager.switch_to(AdminState.complete)
    except AttributeError:
        dialog_manager.dialog_data['complete'] = (
            f'Извините, при удалении {class_name} класса '
            f'что-то пошло не так.\n Вероятно, кто-то уже'
            f'удалил его раньше'
        )
        await dialog_manager.switch_to(AdminState.complete)


async def coef_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    coefs = [
        [coeff.name, coeff.value] for coeff in [
            BASIC, EXAM_BASIC, PRO, EXAM_PRO, MAX
        ]
    ]
    return {'coefs': coefs}


async def coef_value_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    coef_value = dialog_manager.dialog_data['coefs']
    coef_name = next(
        (coef.name for coef in COEFFICIENTS_LIST if str(coef.value) == coef_value),
        None
        )
    getter_data = {'coef_name': coef_name,
                   'coef_value': coef_value}
    print(getter_data)
    return getter_data


async def coef_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    coef_value = dialog_manager.dialog_data['coefs']
    if is_valid_coef(message.text):
        value = float(message.text.replace(",", "."))
        coef = next(
            (coef for coef in COEFFICIENTS_LIST if str(coef.value) == coef_value),
            None
        )
        coef.value = value
        dialog_manager.dialog_data['complete'] = (
            f'Спасибо, коэффициент успешно изменен.\n'
            f'Новое значение {value}'
        )
        await dialog_manager.switch_to(AdminState.complete)
    else:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(
            text='Пожалуйста, введите только число'
                 )


async def complete_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    complete = dialog_manager.dialog_data['complete']
    return {'complete': complete}
