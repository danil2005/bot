from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()


class FSMFillForm(StatesGroup):
    # Анкета
    is_ready_questionnaire = (
        State()
    )  # Состояние ожидания ответа на готовность заполнить анкету
    fill_name = State()  # Состояние ожидания ввода имени
    fill_age = State()  # Состояние ожидания ввода возраста
    fill_gender = State()  # Состояние ожидания выбора пола
    fill_height = State()  # Состояние ожидания ввода роста
    fill_weight = State()  # Состояние ожидания ввода веса
    is_correct_questionnaire = (
        State()
    )  # Состояние ожидания ответа на корректность анкеты

    main_menu = State()  # основное меню

    edite_workouts = State()  # Редактировать тренировки
    archive = State()  # Архивировать тренировки
    delete = State()  # Удалить тренировки
    dearchive = State()  # Восстановить из архива тренировку
    enter_name_workout = State()  # ожидание ввода названия тренировки

    menu_workout = State()
    do_workout = State()
    enter_name_exercise = State()  # ожидание ввода названия упражнения
    do_exercise = State()
    history_exercise = State()
    delete_exercise = State()
    
