from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from filters.fsm import FSMFillForm

from lexicon.lexicon import LEXICON, LEXICON_BUTTON
from keyboards import keyboards
router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        LEXICON[message.text],
        reply_markup=keyboards.keyboard_no_yes
        )
    await state.set_state(FSMFillForm.fill_questionnaire)

#Обработка ответа на вопрос заполнения анкеты
@router.message(StateFilter(FSMFillForm.fill_questionnaire), F.text == LEXICON_BUTTON['yes'])
async def process_yes_questionnaire(message: Message, state: FSMContext):
    await message.answer(
        LEXICON['enter_name'],
        reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(FSMFillForm.fill_name)

@router.message(StateFilter(FSMFillForm.fill_questionnaire), F.text == LEXICON_BUTTON['no'])
async def process_no_questionnaire(message: Message, state: FSMContext):
    await message.answer(
        LEXICON['wait'],
        reply_markup=ReplyKeyboardRemove()
        )
    await state.clear()

@router.message(StateFilter(FSMFillForm.fill_questionnaire))
async def process_other_questionnaire(message: Message):
    await message.answer(
        LEXICON['use_btn_pls'],
        reply_markup=keyboards.keyboard_no_yes
        )

#Имя
@router.message(StateFilter(FSMFillForm.fill_name), lambda x: all(map(str.isalpha, x.text.split())))
async def process_name(message: Message, state: FSMContext):
    await message.answer(LEXICON['enter_age'])
    await state.update_data(name=message.text)
    await state.set_state(FSMFillForm.fill_age)

@router.message(StateFilter(FSMFillForm.fill_name))
async def process_name_error(message: Message):
    await message.answer(LEXICON['error_name'])

#Возраст
@router.message(StateFilter(FSMFillForm.fill_age), F.text.isdigit())
async def process_old(message: Message, state: FSMContext):
    await message.answer(LEXICON['enter_gender'], 
                         reply_markup=keyboards.keyboard_gender)
    await state.update_data(old=message.text)
    await state.set_state(FSMFillForm.fill_gender)

@router.message(StateFilter(FSMFillForm.fill_age))
async def process_old_error(message: Message):
    await message.answer(LEXICON['error_old'])

#Пол
@router.message(StateFilter(FSMFillForm.fill_gender), F.text.in_([LEXICON_BUTTON['male'], LEXICON_BUTTON['female']]))
async def process_gender(message: Message, state: FSMContext):
    await message.answer(LEXICON['enter_height'],
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(gender=message.text)
    await state.set_state(FSMFillForm.fill_height)

@router.message(StateFilter(FSMFillForm.fill_gender))
async def process_gender_error(message: Message):
    await message.answer(LEXICON['use_btn_pls'],
                         reply_markup=keyboards.keyboard_gender)

#Рост
@router.message(StateFilter(FSMFillForm.fill_height), F.text.isdigit())
async def process_height(message: Message, state: FSMContext):
    await message.answer(LEXICON['enter_weight'])
    await state.update_data(height=message.text)
    await state.set_state(FSMFillForm.fill_weight)

@router.message(StateFilter(FSMFillForm.fill_height))
async def process_height_error(message: Message):
    await message.answer(LEXICON['error_height'])

#Вес
@router.message(StateFilter(FSMFillForm.fill_weight), F.text.isdigit())
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Хуй')
    #await state.set_state(FSMFillForm.fill_weight)

@router.message(StateFilter(FSMFillForm.fill_height))
async def process_weight_error(message: Message):
    await message.answer(LEXICON['error_weight'])

