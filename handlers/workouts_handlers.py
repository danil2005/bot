from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from filters.fsm import FSMFillForm

from lexicon.lexicon import LEXICON, LEXICON_MAIN_MENU
from keyboards import keyboards
from database import database

router = Router()

#Отладочное
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        LEXICON['menu'],
        reply_markup=keyboards.inline_kb_main_menu(message.chat.id))
    await state.set_state(FSMFillForm.main_menu)

#Редкатировать тренировки
@router.callback_query(StateFilter(FSMFillForm.main_menu), F.data == 'edit_workouts')
async def process_edite_workouts(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=LEXICON_MAIN_MENU['edit_workouts'],
                                     reply_markup=keyboards.inline_kb_edit_workouts)
    await state.set_state(FSMFillForm.edite_workouts)

#Создать тренировку
@router.callback_query(StateFilter(FSMFillForm.edite_workouts), F.data == 'create_workout')
async def process_create_workout(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(LEXICON['enter_name_workout'])
    await state.set_state(FSMFillForm.enter_name_workout)

#Обработка ввода названия новой тренировки
@router.message(StateFilter(FSMFillForm.enter_name_workout))
async def process_enter_name_workout(message: Message, state: FSMContext):
    if (database.add_new_workout(message.chat.id, message.text)):
        await message.answer(LEXICON['menu'],
                             reply_markup=keyboards.inline_kb_main_menu(message.chat.id))
        await state.set_state(FSMFillForm.main_menu)
    else:
        await message.answer(LEXICON['repeat_name_workout'])

#Архивировать
@router.callback_query(StateFilter(FSMFillForm.edite_workouts), F.data == 'archive')
async def process_archive_workout(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=LEXICON['select_archive'],
                                     reply_markup=keyboards.inline_kb_archive_workouts(callback.message.chat.id))
    await state.set_state(FSMFillForm.archive)

@router.callback_query(StateFilter(FSMFillForm.archive), F.data.isdigit())
async def process_archive_select(callback: CallbackQuery):
    await callback.answer()




    
    
    


