from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from filters.fsm import FSMFillForm

from lexicon.lexicon import LEXICON
from lexicon import lexicon
from keyboards import keyboards
from database import database

router = Router()


# Меню тренировки
@router.callback_query(StateFilter(FSMFillForm.main_menu), F.data.isdigit())
async def process_menu_workout(callback: CallbackQuery, state: FSMContext):
    await state.update_data(workout_type=callback.data)
    await callback.answer()
    await callback.message.edit_text(
        text=lexicon.workout_type_text(callback.data),
        reply_markup=keyboards.inline_kb_menu_workouts(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.menu_workout)


# Вернуться в меню
@router.callback_query(StateFilter(FSMFillForm.menu_workout), F.data == "main_menu")
async def process_back_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        LEXICON["menu"],
        reply_markup=keyboards.inline_kb_main_menu(callback.message.chat.id),
    )
    await state.clear()
    await state.set_state(FSMFillForm.main_menu)


# Старт тренировки
@router.callback_query(StateFilter(FSMFillForm.menu_workout), F.data == "start")
async def process_do_workout(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_workout = database.start_workout(callback.message.chat.id, data["workout_type"])
    await state.update_data(
        workout=id_workout,
        completed_exercises=[],
        message_id=callback.message.message_id,
    )
    await callback.answer()
    await callback.message.edit_text(
        text=lexicon.workout_type_text(data["workout_type"]),
        reply_markup=keyboards.inline_kb_do_workout(data["workout_type"]),
    )
    await state.set_state(FSMFillForm.do_workout)


# Выбор упражнения по кнопке
@router.callback_query(StateFilter(FSMFillForm.do_workout), F.data.isdigit())
async def process_select_exercise(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_exercise = database.start_exercise(callback.data, data["workout"])
    await callback.message.edit_text(
        text=lexicon.workout_type_text(data["workout_type"]),
        reply_markup=keyboards.inline_kb_do_exercise(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.do_exercise)
    data["completed_exercises"].append(callback.data)
    await state.update_data(
        exercise_type=int(callback.data),
        exercise=id_exercise,
        completed_exercises=data["completed_exercises"],
    )


# Новое упражнение
@router.callback_query(StateFilter(FSMFillForm.do_workout), F.data == "new")
async def process_new_exercise(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # await callback.message.delete()
    await callback.message.answer(LEXICON["enter_name_exercise"])
    await state.set_state(FSMFillForm.enter_name_exercise)


# Конец тренировки
@router.callback_query(StateFilter(FSMFillForm.do_workout), F.data == "end")
async def process_end_workout(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer()
    database.end_workout(data["workout"])
    await callback.message.delete()
    await callback.message.answer(lexicon.workout_end_text(data["workout"]))
    await callback.message.answer(
        LEXICON["menu"],
        reply_markup=keyboards.inline_kb_main_menu(callback.message.chat.id),
    )
    await state.clear()
    await state.set_state(FSMFillForm.main_menu)


# Другое упражнение
@router.callback_query(StateFilter(FSMFillForm.do_workout), F.data == "other")
async def process_other_exercise(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer()
    await callback.message.edit_text(
        text=lexicon.workout_type_text(data["workout_type"]),
        reply_markup=keyboards.inline_kb_other_exercise(
            callback.message.chat.id, data["workout_type"]
        ),
    )
    await state.set_state(FSMFillForm.do_workout)


# Вернуться из "Другое упражнение"
@router.callback_query(StateFilter(FSMFillForm.do_workout), F.data == "back")
async def process_back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer()
    await callback.message.edit_text(
        text=lexicon.workout_type_text(data["workout_type"]),
        reply_markup=keyboards.inline_kb_do_workout(data["workout_type"]),
    )

# Другое упражнение
@router.callback_query(StateFilter(FSMFillForm.do_workout), F.data == "delete")
async def process_delete_exercise(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON['delete_exercise'],
        reply_markup=keyboards.inline_kb_delete_exercise(
            callback.message.chat.id, data["workout"]
        )
    )
    await state.set_state(FSMFillForm.do_workout)

# Ввод названия упражнения
@router.message(StateFilter(FSMFillForm.enter_name_exercise))
async def process_enter_name_exercise(message: Message, state: FSMContext):
    id_exercise_type = database.add_new_exercise(message.chat.id, message.text)
    await message.bot.delete_message(message.chat.id, message.message_id)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    if id_exercise_type:
        data = await state.get_data()
        id_exercise = database.start_exercise(id_exercise_type, data["workout"])
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text=lexicon.workout_type_text(data["workout_type"]),
            reply_markup=keyboards.inline_kb_do_exercise(message.chat.id),
        )
        await state.set_state(FSMFillForm.do_exercise)
        await state.update_data(
            exercise_type=int(id_exercise_type), exercise=id_exercise
        )
    else:
        await message.answer(LEXICON["repeat_name_exercise"])


# Выполнение упражнения
@router.message(StateFilter(FSMFillForm.do_exercise))
async def process_do_exercise(message: Message, state: FSMContext):
    data = await state.get_data()
    database.update_exercise(data["exercise"], message.text)
    await message.bot.delete_message(message.chat.id, message.message_id)
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["message_id"],
        text=lexicon.workout_type_text(data["workout_type"]),
        reply_markup=keyboards.inline_kb_do_exercise(message.chat.id),
    )


# Закончить упражнение
@router.callback_query(StateFilter(FSMFillForm.do_exercise), F.data == "finish")
async def process_end_exercise(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text(
        text=lexicon.workout_type_text(data["workout_type"]),
        reply_markup=keyboards.inline_kb_do_workout(
            data["workout_type"], data["completed_exercises"]
        ),
    )
    await state.set_state(FSMFillForm.do_workout)


# История упражнения
@router.callback_query(StateFilter(FSMFillForm.do_exercise), F.data == "history")
async def process_history_exercise(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text(
        text=lexicon.history_exercise(data["exercise_type"]),
        reply_markup=keyboards.inline_kb_history_exercise(),
    )
    await state.set_state(FSMFillForm.history_exercise)


# Назад из истории упражнения
@router.callback_query(StateFilter(FSMFillForm.history_exercise), F.data == "back")
async def process_back_history_exercise(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text(
        text=lexicon.workout_type_text(data["workout_type"]),
        reply_markup=keyboards.inline_kb_do_exercise(callback.message.chat.id),
    )
    await state.set_state(FSMFillForm.do_exercise)
