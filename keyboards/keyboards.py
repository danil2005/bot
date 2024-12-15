from lexicon import lexicon
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import database

def create_keyboard(*names: str):
    buttons = [KeyboardButton(text=i) for i in names]
    return ReplyKeyboardMarkup(keyboard=[buttons],
                               resize_keyboard=True,
                               one_time_keyboard=True)

keyboard_no_yes = create_keyboard(lexicon.LEXICON_BUTTON['yes'], lexicon.LEXICON_BUTTON['no'])
keyboard_gender = create_keyboard(lexicon.LEXICON_BUTTON['male'], lexicon.LEXICON_BUTTON['female'])

def create_inline_keyboard (data):
    buttons = [InlineKeyboardButton(callback_data=d, text=t) for d,t in data]
    ikb_builder = InlineKeyboardBuilder()
    ikb_builder.row(*buttons, width=1)
    return ikb_builder.as_markup()

def inline_kb_main_menu(id: int) -> InlineKeyboardMarkup:
    workouts = database.get_active_workout(id)
    workouts = [(str(i), j) for i,j in workouts]
    data = workouts + list(lexicon.LEXICON_MAIN_MENU.items())
    return create_inline_keyboard(data)

inline_kb_edit_workouts = create_inline_keyboard(lexicon.LEXICON_EDIT_WORKOUTS.items())

def inline_kb_archive_workouts(id: int) -> InlineKeyboardMarkup:
    workouts = database.get_active_workout(id)
    workouts = [(str(i), j) for i,j in workouts]
    data = workouts + list(lexicon.LEXICON_ARCHIVE_MENU.items())
    return create_inline_keyboard(data)






