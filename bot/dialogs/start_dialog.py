from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const, Format

from dialog_hadlers.start_dialog_handlers import username_getter
from .filters import is_admin
from fsm.fsm_dialogs import (
    AdminState, StartState, QuestionnaireState
    )


start_dialog = Dialog(
    Window(
        Format('<b>Приветствую, {username}!</b>\n'),
        Const('Это бот, в котором девятиклассники школы Интеллектуал '
              'могут оценить перспективы успешного перехода в 10 класс.\n'
              'Для этого нажмите на кнопку ниже и ответьте на вопросы.'),
        Start(Const('Опрос'), id='questionnaire_first',
              state=QuestionnaireState.first_name, when='first_show'),
        Start(Const('Опрос'), id='questionnaire_again',
              state=QuestionnaireState.first_subject, when='second_show'),
        Start(Const('Админка'), id='admin',
              state=AdminState.start, when=is_admin),
        getter=username_getter,
        state=StartState.start,
        ),
    )
