from lexicon.lexicon import LEXICON_BUTTON, LEXICON_MAIN_MENU
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_keyboard(*names: str):
    buttons = [KeyboardButton(text=i) for i in names]
    return ReplyKeyboardMarkup(keyboard=[buttons],
                               resize_keyboard=True,
                               one_time_keyboard=True)

keyboard_no_yes = create_keyboard(LEXICON_BUTTON['yes'], LEXICON_BUTTON['no'])
keyboard_gender = create_keyboard(LEXICON_BUTTON['male'], LEXICON_BUTTON['female'])

def create_inline_keyboard (data : dict):
    buttons = [InlineKeyboardButton(callback_data=d, text=t) for d,t in data.items()]
    ikb_builder = InlineKeyboardBuilder()
    ikb_builder.row(*buttons, width=1)
    return ikb_builder.as_markup()

inline_kb_main_menu = create_inline_keyboard(LEXICON_MAIN_MENU)


