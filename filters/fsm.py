from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

class FSMFillForm(StatesGroup):
    is_ready_questionnaire = State()        # Состояние ожидания ответа на готовность заполнить анкету
    fill_name = State()        # Состояние ожидания ввода имени
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_gender = State()      # Состояние ожидания выбора пола
    fill_height = State()      # Состояние ожидания ввода роста
    fill_weight = State()      # Состояние ожидания ввода веса
    is_correct_questionnaire = State()      # Состояние ожидания ответа на корректность анкеты
    questionnaire_ready = State()      # анкета готова

