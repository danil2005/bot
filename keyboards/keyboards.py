from lexicon.lexicon import LEXICON_BUTTON
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# _b_yes = KeyboardButton(text=LEXICON_BUTTON['yes'])
# _b_no = KeyboardButton(text=LEXICON_BUTTON['no'])

# keyboard_no_yes = ReplyKeyboardMarkup(
#     keyboard=[[_b_no, _b_yes]],
#     resize_keyboard=True,
#     one_time_keyboard=True
# )

def create_keyboard(*names: str):
    buttons = [KeyboardButton(text=i) for i in names]
    return ReplyKeyboardMarkup(keyboard=[buttons],
                               resize_keyboard=True,
                               one_time_keyboard=True)

keyboard_no_yes = create_keyboard(LEXICON_BUTTON['yes'], LEXICON_BUTTON['no'])
keyboard_gender = create_keyboard(LEXICON_BUTTON['male'], LEXICON_BUTTON['female'])



