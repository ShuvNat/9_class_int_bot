from aiogram.enums import ContentType
from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Back, Button, Cancel, Group, Row, Select, Start, SwitchTo
)
from aiogram_dialog.widgets.text import Const, Format
from operator import itemgetter

from dialog_hadlers.admin_dialog_handlers import (
    class_getter, class_add_handler, class_delete_handler, class_name_getter,
    class_rename_handler, coef_getter, coef_handler, coef_value_getter,
    complete_getter, get_xlsx_file, select_handler, user_getter
)
from fsm.fsm_dialogs import AdminState, StartState
from .filters import is_admin


admin_dialog = Dialog(
    Window(
        Const('Что вы хотите сделать?'),
        Button(Const('Скачать файл данных'), id='statistic',
               when=is_admin, on_click=get_xlsx_file),
        SwitchTo(Const('Изменить классы'), id='classes_choice_action',
                 state=AdminState.classes_choise_action, when=is_admin),
        SwitchTo(Const('Изменить коэффициенты'), id='coef_change',
                 state=AdminState.coef_choice, when=is_admin),
        Start(Const('На старт'), id='start', state=StartState.start,
              mode=StartMode.RESET_STACK),
        getter=user_getter,
        state=AdminState.start,
        ),
    Window(
        Const('Измение классов никак не затронет данные,'
              'уже хранящиеся в базе'),
        SwitchTo(Const('Переименовать класс'), id='rename',
                 state=AdminState.classes_choise_class),
        SwitchTo(Const('Удалить класс'), id='del',
                 state=AdminState.delete_class),
        SwitchTo(Const('Добавить класс'), id='add',
                 state=AdminState.add_class),
        Row(
            Back(Const('Назад'), id='back'),
            Start(Const('На старт'), id='start', state=StartState.start,
                  mode=StartMode.RESET_STACK),
        ),
        state=AdminState.classes_choise_action,
    ),
    Window(
        Const('Какой класс вы хотите переименовать'),
        Group(
            Select(
                Format("{item[1]}"),
                id="class_letter",
                items="classes",
                item_id_getter=itemgetter(0),
                on_click=select_handler
            ),
            width=2
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        getter=class_getter,
        state=AdminState.classes_choise_class,
    ),
    Window(
        Const('Введите новое название класса в формате 9А'),
        MessageInput(
            func=class_rename_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            SwitchTo(Const('Назад'), id='back',
                     state=AdminState.classes_choise_class),
        ),
        state=AdminState.rename_class,
    ),
    Window(
        Const('Какой класс вы хотите удалить'),
        Group(
            Select(
                Format("{item[1]}"),
                id="class_letter",
                items="classes",
                item_id_getter=itemgetter(0),
                on_click=select_handler
            ),
            width=2
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            SwitchTo(Const('Назад'), id='back',
                     state=AdminState.classes_choise_class),
        ),
        getter=class_getter,
        state=AdminState.delete_class,
    ),
    Window(
        Format('Пожалуйста, подтвердите удаление {class_name} класса'),
        Row(
            Button(Const('Да'), id='yes', on_click=class_delete_handler),
            Back(Const('Нет'), id='no')
        ),
        getter=class_name_getter,
        state=AdminState.delete_class_confirm,
    ),
    Window(
        Const('Введите название нового класса в формате 9А'),
        MessageInput(
            func=class_add_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            SwitchTo(Const('Назад'), id='back',
                     state=AdminState.classes_choise_action),
        ),
        state=AdminState.add_class,
    ),
    Window(
        Const('Измения коэффициентов никак не затронут данные,'
              'хранящиеся в базе\n\n'
              'Какой коэффициент вы хотите изменить?'),
        Group(
            Select(
                Format("{item[0]}"),
                id="coefs",
                items="coefs",
                item_id_getter=itemgetter(1),
                on_click=select_handler
            ),
            width=2
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            SwitchTo(Const('Назад'), id='back',
                     state=AdminState.start),
        ),
        getter=coef_getter,
        state=AdminState.coef_choice,
    ),
    Window(
        Format('Сейчас значение коэффициента {coef_name}: {coef_value}\n'
               'Введите новое значение'),
        MessageInput(
            func=coef_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            SwitchTo(Const('Назад'), id='back',
                     state=AdminState.coef_choice),
        ),
        getter=coef_value_getter,
        state=AdminState.coeff_change,
    ),
    Window(
        Format('{complete}'),
        SwitchTo(Const('В Админку'), id='back',
                 state=AdminState.start),
        Start(Const('На старт'), id='start', state=StartState.start,
              mode=StartMode.RESET_STACK),
        getter=complete_getter,
        state=AdminState.complete,
    )
)
