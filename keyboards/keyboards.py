from lexicon import lexicon
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import database


def create_keyboard(*names: str):
    buttons = [KeyboardButton(text=i) for i in names]
    return ReplyKeyboardMarkup(
        keyboard=[buttons], resize_keyboard=True, one_time_keyboard=True
    )


keyboard_no_yes = create_keyboard(
    lexicon.LEXICON_BUTTON["yes"], lexicon.LEXICON_BUTTON["no"]
)
keyboard_gender = create_keyboard(
    lexicon.LEXICON_BUTTON["male"], lexicon.LEXICON_BUTTON["female"]
)


def create_inline_keyboard(data):
    buttons = [InlineKeyboardButton(callback_data=d, text=t) for d, t in data]
    ikb_builder = InlineKeyboardBuilder()
    ikb_builder.row(*buttons, width=1)
    return ikb_builder.as_markup()


def inline_kb_main_menu(id: int) -> InlineKeyboardMarkup:
    workouts = database.get_active_workouts(id)
    workouts = [(str(i), j) for i, j in workouts]
    data = workouts + list(lexicon.LEXICON_MAIN_MENU.items())
    return create_inline_keyboard(data)


inline_kb_edit_workouts = create_inline_keyboard(lexicon.LEXICON_EDIT_WORKOUTS.items())


def inline_kb_archive_workouts(id: int) -> InlineKeyboardMarkup:
    workouts = database.get_active_workouts(id)
    workouts = [(str(i), j) for i, j in workouts]
    data = workouts + list(lexicon.LEXICON_EDIT_ACTION.items())
    return create_inline_keyboard(data)


def inline_kb_delete_workouts(id: int) -> InlineKeyboardMarkup:
    workouts = database.get_all_workouts(id)
    workouts = [(str(i), j) for i, j in workouts]
    data = workouts + list(lexicon.LEXICON_EDIT_ACTION.items())
    return create_inline_keyboard(data)


def inline_kb_dearchive_workouts(id: int) -> InlineKeyboardMarkup:
    workouts = database.get_deactive_workouts(id)
    workouts = [(str(i), j) for i, j in workouts]
    data = workouts + list(lexicon.LEXICON_EDIT_ACTION.items())
    return create_inline_keyboard(data)


def inline_kb_menu_workouts(id: int) -> InlineKeyboardMarkup:
    data = list(lexicon.WORKOUT_MENU.items())
    return create_inline_keyboard(data)


def inline_kb_do_workout(
    type_workout: int, completed_exercises: list[int] = []
) -> InlineKeyboardMarkup:
    exercises = database.get_workout_exercises(type_workout)
    exercises = [i for i in exercises if i[0] not in completed_exercises]
    data = exercises + list(lexicon.START_WORKOUT.items())
    return create_inline_keyboard(data)


def inline_kb_do_exercise(id: int) -> InlineKeyboardMarkup:
    data = list(lexicon.DO_EXERCISE.items())
    return create_inline_keyboard(data)


def inline_kb_other_exercise(chat_id: int, type_workout: int):
    exercises = database.get_all_exercises(chat_id)
    current_exercises = database.get_workout_exercises(type_workout)
    current_exercises = [i[0] for i in current_exercises]
    exercises = [i for i in exercises if i[0] not in current_exercises]
    return create_inline_keyboard(exercises + list(lexicon.OTHER_EXERCISE.items()))


def inline_kb_history_exercise() -> InlineKeyboardMarkup:
    data = list(lexicon.HISTORY_EXERCISE.items())
    return create_inline_keyboard(data)

def inline_kb_delete_exercise (chat_id: int, workout_id: int):
    
