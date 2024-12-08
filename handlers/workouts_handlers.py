from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from filters.fsm import FSMFillForm

from lexicon.lexicon import LEXICON, LEXICON_BUTTON
from keyboards import keyboards
from services.services import create_questionnaire_text
from database.database import add_questionnaire_db

router = Router()


