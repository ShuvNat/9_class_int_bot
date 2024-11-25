from aiogram.enums import ContentType
from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Group, Cancel, Row, Select, Start
from aiogram_dialog.widgets.text import Case, Const, Format
from operator import itemgetter

from fsm.fsm_dialogs import StartState, QuestionnaireState
from dialog_hadlers.questionary_dialog_handlers import (
    class_getter, class_handler, exam_grade_handler, first_name_handler,
    grade_handler, group_getter, last_name_handler, olymp_getter,
    result_getter, select_handler, subject_getter,
)


questionnaire_dialog = Dialog(
    Window(
        Const('Пожалуйста, ответьте несколько вопросов'),
        Const('1. Напишите ваше имя'),
        Cancel(Const('Отмена'), id='cancel'),
        MessageInput(
            func=first_name_handler,
            content_types=ContentType.TEXT,
        ),
        state=QuestionnaireState.first_name,
    ),
    Window(
        Const('2. Напишите вашу фамилию'),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        MessageInput(
            func=last_name_handler,
            content_types=ContentType.TEXT,
        ),
        state=QuestionnaireState.last_name,
    ),
    Window(
        Const('3. В каком классе вы учитесь'),
        Group(
            Select(
                Format("{item[1]}"),
                id="class_letter",
                items="classes",
                item_id_getter=itemgetter(0),
                on_click=class_handler
            ),
            width=2
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        getter=class_getter,
        state=QuestionnaireState.class_letter,
    ),
    Window(
        Const('4. Выберите один из профильных предметов'),
        Group(
            Select(
                Format("{item[0]}"),
                id="first_subject",
                items="subjects",
                item_id_getter=itemgetter(0),
                on_click=select_handler
            ),
            width=2
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        getter=subject_getter,
        state=QuestionnaireState.first_subject,
    ),
    Window(
        Const('5. В какой вы группе по этому предмету?'),
        Group(
            Select(
                Format("{item[0]}"),
                id="first_subject_group",
                items="groups",
                item_id_getter=itemgetter(0),
                on_click=select_handler
            ),
            width=3
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        getter=group_getter,
        state=QuestionnaireState.first_subject_group,
    ),
    Window(
        Const('6. Какая у вас реальная или ожидаемая оценка за 1 полугодие?\n'
              'Напишите число от 1 до 5 с точностью до сотых'),
        MessageInput(
            func=grade_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        state=QuestionnaireState.first_subject_firsts_grade,
    ),
    Window(
        Const('7. Какая у вас реальная или ожидаемая оценка за 2 полугодие?\n'
              'Напишите число от 1 до 5 с точностью до сотых'),
        MessageInput(
            func=grade_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        state=QuestionnaireState.first_subject_second_grade,
    ),
    Window(
        Const('8. Какую оценку вы ожидаете на экзамене по этому предмету?\n'
              'Напишите целое число от 0 до 10'),
        MessageInput(
            func=exam_grade_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        state=QuestionnaireState.first_subject_exam_grade,
    ),
    Window(
        Const('9. Выберите второй профильный предмет'),
        Group(
            Select(
                Format("{item[0]}"),
                id="second_subject",
                items="subjects",
                item_id_getter=itemgetter(0),
                on_click=select_handler
            ),
            width=2
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        getter=subject_getter,
        state=QuestionnaireState.second_subject,
    ),
    Window(
        Const('10. В какой вы группе по этому предмету?'),
        Group(
            Select(
                Format("{item[0]}"),
                id="second_subject_group",
                items="groups",
                item_id_getter=itemgetter(0),
                on_click=select_handler
            ),
            width=3
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        getter=group_getter,
        state=QuestionnaireState.second_subject_group,
    ),
    Window(
        Const('11. Какая у вас реальная или ожидаемая оценка за 1 полугодие?\n'
              'Напишите число от 1 до 5 с точностью до сотых'),
        MessageInput(
            func=grade_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        state=QuestionnaireState.second_subject_firsts_grade,
    ),
    Window(
        Const('12. Какая у вас реальная или ожидаемая оценка за 2 полугодие?\n'
              'Напишите число от 1 до 5 с точностью до сотых'),
        MessageInput(
            func=grade_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        state=QuestionnaireState.second_subject_second_grade,
    ),
    Window(
        Const('13. Какую оценку вы ожидаете на экзамене по этому предмету?\n'
              'Напишите целое число от 0 до 10'),
        MessageInput(
            func=exam_grade_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        state=QuestionnaireState.second_subject_exam_grade,
    ),
    Window(
        Const('14. Были ли вы призером или победителем во Всероссийской '
              'олимпиаде по какому-то предмету в 9 классе?'),
        Group(
            Select(
                Format("{item[0]}"),
                id="olymp",
                items="olymp",
                item_id_getter=itemgetter(0),
                on_click=select_handler
            ),
            width=2
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        getter=olymp_getter,
        state=QuestionnaireState.olymp,
    ),
    Window(
        Const('15. Какой средний балл аттестата за 9 класс вы ожидаете?\n'
              'Имеется в виду средний балл по всем предметам\n'
              'Напишите число от 1 до 5 с точностью до сотых'),
        MessageInput(
            func=grade_handler,
            content_types=ContentType.TEXT,
        ),
        Row(
            Cancel(Const('Отмена'), id='cancel'),
            Back(Const('Назад'), id='back'),
        ),
        state=QuestionnaireState.year_average_grade,
    ),
    Window(
        Format('Спасибо, {real_name}\n'
               'Ваш результат: {result:.0f}% \n'),
        Case(
            texts={
                1: Const('С переходом в 10 класс будут серьезные '
                         'проблемы, нужно <b>обязательно</b> поговорить с '
                         'классным руководителем или завучем.\n\n'),
                2: Const('С переходом в 10 класс будут сложности. '
                         'Нужно поговорить с классным руководителем или '
                         'завучем и попросить помощи у учителей групп по '
                         'профильным предметам.\n\n'),
                3: Const('С переходом в 10 класс возможны сложности. '
                         'Имеет смысл поговорить с классным руководителем '
                         'и учителями групп по профильным предметам.\n\n'),
                4: Const('С переходом в 10 класс, скорее всего, все будет '
                         'хорошо, но, возможно, есть места, которые '
                         'стоит усилить.\nПоговорите о них с учителями '
                         'групп по профильным предметам.\n\n'),
                5: Const('С переходом в 10 класс все будет хорошо.\n\n')
            },
            selector='text'
        ),
        Const('Если вы указали что-то неправильно,\n'
              'или просто захотите обновить информацию,\n'
              'анкета всегда доступна в стартовом меню.\n'),
        Start(Const('На старт'), id='start', state=StartState.start,
              mode=StartMode.RESET_STACK),
        getter=result_getter,
        state=QuestionnaireState.save,
    ),
)
