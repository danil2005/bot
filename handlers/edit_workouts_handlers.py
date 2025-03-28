from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from filters.fsm import FSMFillForm

from lexicon import lexicon
from lexicon.lexicon import LEXICON
from keyboards import keyboards
from database import database

router = Router()


# Отладочное
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        LEXICON["menu"], reply_markup=await keyboards.inline_kb_main_menu(message.chat.id)
    )
    await state.clear()
    await state.set_state(FSMFillForm.main_menu)


# Редкатировать тренировки
@router.callback_query(StateFilter(FSMFillForm.main_menu), F.data == "edit_workouts")
async def process_edite_workouts(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=lexicon.MAIN_MENU["edit_workouts"],
        reply_markup=keyboards.inline_kb_edit_workouts(),
    )
    await state.set_state(FSMFillForm.edite_workouts)


# Вернуться в меню
@router.callback_query(StateFilter(FSMFillForm.edite_workouts), F.data == "main_menu")
async def process_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        LEXICON["menu"],
        reply_markup=await keyboards.inline_kb_main_menu(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.main_menu)


# Создать тренировку
@router.callback_query(
    StateFilter(FSMFillForm.edite_workouts), F.data == "create_workout"
)
async def process_create_workout(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(LEXICON["enter_name_workout"])
    await state.set_state(FSMFillForm.enter_name_workout)
    await state.update_data(message_id=callback.message.message_id + 1)


@router.message(StateFilter(FSMFillForm.enter_name_workout))
async def process_enter_name_workout(message: Message, state: FSMContext):
    if await database.add_new_workout_type(message.chat.id, message.text):
        data = await state.get_data()
        for i in range(data['message_id'], message.message_id + 1):
            await message.bot.delete_message(message.chat.id, i)

        await message.answer(
            LEXICON["menu"], reply_markup=await keyboards.inline_kb_main_menu(message.chat.id)
        )
        await state.set_state(FSMFillForm.main_menu)
    else:
        await message.answer(LEXICON["repeat_name_workout"])


# Архивировать
@router.callback_query(StateFilter(FSMFillForm.edite_workouts), F.data == "archive")
async def process_archive_workout(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON["select_archive"],
        reply_markup=await keyboards.inline_kb_archive_workouts(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.archive)


@router.callback_query(StateFilter(FSMFillForm.archive), F.data.isdigit())
async def process_archive_select(callback: CallbackQuery):
    await database.set_active_workout_type(int(callback.data), False)
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON["select_archive"],
        reply_markup=await keyboards.inline_kb_archive_workouts(callback.message.chat.id),
    )


@router.callback_query(StateFilter(FSMFillForm.archive), F.data == "ready")
async def process_archive_ready(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        LEXICON["menu"],
        reply_markup=await keyboards.inline_kb_main_menu(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.main_menu)


# Удалить
@router.callback_query(StateFilter(FSMFillForm.edite_workouts), F.data == "delete")
async def process_delete_workout(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON["delete"],
        reply_markup=await keyboards.inline_kb_delete_workouts(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.delete)


@router.callback_query(StateFilter(FSMFillForm.delete), F.data.isdigit())
async def process_delete_select(callback: CallbackQuery):
    await database.delete_workout_type(int(callback.data))
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON["delete"],
        reply_markup=await keyboards.inline_kb_delete_workouts(callback.message.chat.id),
    )


@router.callback_query(StateFilter(FSMFillForm.delete), F.data == "ready")
async def process_delete_ready(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        LEXICON["menu"],
        reply_markup=await keyboards.inline_kb_main_menu(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.main_menu)


# Восстановить из архива
@router.callback_query(StateFilter(FSMFillForm.edite_workouts), F.data == "dearchive")
async def process_dearchive_workout(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON["dearchive"],
        reply_markup=await keyboards.inline_kb_dearchive_workouts(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.dearchive)


@router.callback_query(StateFilter(FSMFillForm.dearchive), F.data.isdigit())
async def process_dearchive_select(callback: CallbackQuery):
    await database.set_active_workout_type(int(callback.data), True)
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON["dearchive"],
        reply_markup=await keyboards.inline_kb_dearchive_workouts(callback.message.chat.id),
    )


@router.callback_query(StateFilter(FSMFillForm.dearchive), F.data == "ready")
async def process_dearchive_ready(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        LEXICON["menu"],
        reply_markup=await keyboards.inline_kb_main_menu(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.main_menu)
