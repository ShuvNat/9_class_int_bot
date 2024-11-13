from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage, Redis

redis = Redis(host='localhost', port=6379, db=5)

storage = RedisStorage(
    redis=redis,
    key_builder=DefaultKeyBuilder(with_destiny=True)
    )


class StartState(StatesGroup):
    start = State()


class QuestionnaireState(StatesGroup):
    first_name = State()
    last_name = State()
    class_letter = State()
    first_subject = State()
    first_subject_group = State()
    first_subject_firsts_grade = State()
    first_subject_second_grade = State()
    first_subject_exam_grade = State()
    second_subject = State()
    second_subject_group = State()
    second_subject_firsts_grade = State()
    second_subject_second_grade = State()
    second_subject_exam_grade = State()
    olymp = State()
    year_average_grade = State()
    save = State()


class AdminState(StatesGroup):
    start = State()
    classes_choise_action = State()
    classes_choise_class = State()
    rename_class = State()
    add_class = State()
    delete_class = State()
    delete_class_confirm = State()
    coef_choice = State()
    coeff_change = State()
    basic = State()
    exam_basic = State()
    pro = State()
    exam_pro = State()
    max = State()
    complete = State()
