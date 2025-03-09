from database import database
from datetime import datetime

LEXICON: dict[str, str] = {
    "/start": "Привет! Этот бот поможет вести статистику тренировок.\n"
    "Мне нужны некоторые данные о Вас.\n"
    "Вы готовы ответить на пару вопросов?",
    "enter_name": "Введите полное имя.",
    "error_name": "Имя должно сосоять только из букв.",
    "enter_age": "Введите возраст.",
    "error_old": "Возраст должен состоять только из цифр",
    "enter_gender": "Введите пол.",
    "enter_height": "Введите рост.",
    "error_height": "Рост должен состоять только из цифр.",
    "enter_weight": "Введите вес.",
    "error_weight": "Вес должен состоять только из цифр.",
    "use_btn_pls": "Воспользуйтесь пожалуйста кнопками снизу.",
    "wait": "Если передумаете, просто нажмите кнопку /start.",
    "questionnaire_ready": "Анкета готова!\nТеперь можно начать составлять программы тренировок и тренироваться.",
    "questionnaire_again": "Тогда давайте заполним анкету заново.",
    "menu": "Меню",
    "enter_name_workout": "Введите название тренировки",
    "create_workout_success": "Тренировкка создана",
    "repeat_name_workout": "Тренировка с таким названием уже существует.\nВведите другое название либо удалите тренировку с таким же названием.",
    "select_archive": "Выберите тренировки для архивации",
    "delete": "Выберите тренировки для удаления",
    "dearchive": "Выберите тренировки для восстановления из архива",
    "workout": "Тренировка:",
    "enter_name_exercise": "Введите название упражнения",
    "repeat_name_exercise": "Упражнение с таким названием уже существует.\nВведите другое название.",
    "delete_exercise": "Выберите упражнение для удаления"
}

LEXICON_COMMANDS: dict[str, str] = {
    "/start": "🚀 Старт 🚀",
    "/help": "📖 Справка по работе бота 📖",
}

LEXICON_BUTTON: dict[str, str] = {
    "yes": "✅ ДА ✅",
    "no": "❌ НЕТ ❌",
    "male": "👨 Мужской 👨",
    "female": "👩 Женский 👩",
}

LEXICON_MAIN_MENU: dict[str, str] = {
    "edit_workouts": "⚙️ Редактировать тренировки ⚙️",
    # 'fix_weight': '⚖️ Зафиксировать вес ⚖️'
}

LEXICON_EDIT_ACTION: dict[str, str] = {"ready": "✔️ Готово ✔️"}

LEXICON_EDIT_WORKOUTS: dict[str, str] = {
    "create_workout": "➕ Создать ➕",
    "archive": "📥 Архивировать 📥",
    "delete": "🗑️ Удалить 🗑️",
    "dearchive": "📤 Добавить из архива 📤",
    "main_menu": "🏠 Главное меню 🏠",
}

WORKOUT_MENU: dict[str, str] = {
    "start": "▶️ Старт ▶️",
    # 'watch': '👀 Просмотр 👀',
    "main_menu": "🏠 Главное меню 🏠",
}

START_WORKOUT: dict[str, str] = {
    "new": "🆕 Новое упражнение 🆕",
    "other": "🔄 Другое упражнение 🔄",
    "delete": "🗑️ Удалить строку 🗑️",
    "end": "🏁 Конец тренировки 🏁",
}

DO_EXERCISE: dict[str, str] = {
    "finish": "✅ Закончить упражнение ✅",
    "history": "📜 История 📜",
}

OTHER_EXERCISE: dict[str, str] = {
    "back": "↩️ Назад ↩️",
}

HISTORY_EXERCISE: dict[str, str] = {
    "back": "↩️ Назад ↩️",
}

DELETE_EXERCISE: dict[str, str] = {
    "back": "↩️ Назад ↩️",
}

async def weight_workout(id):
    data = await database.get_weight_workout(id)
    return "\n".join([f"{i}: {j}" for i, j, _ in data])


async def workout_type_text(type_workout: int):
    res = await database.get_name_workout(type_workout) + "\n\n"
    # получаем id последних тренировок
    ids = await database.get_latest_workout_ids(type_workout)
    ids.reverse()
    for i in ids:
        date = await database.get_date_workout(i)
        weights = await weight_workout(i)
        res += date + "\n" + weights + "\n\n"

    return res


async def workout_end_text(workout_id: int):
    info = await database.get_info_workout(workout_id)
    name = await database.get_name_workout(info[3])

    # date_start = datetime.strptime(info[0], "%d-%m-%Y").date()
    # time_start = datetime.strptime(info[1], "%H:%M:%S").time()
    # start = datetime.combine(date_start, time_start)
    # start_text = start.strftime("%d.%m.%y %H:%M")

    res = f"{name}\nПродолжительность - {info[2]} мин\n\n" + await weight_workout(workout_id)

    return res


async def history_exercise(id_type: int):
    data = await database.get_history(id_type)
    res = ""
    for name, date, time, weights in data:
        res += f"{name}. {date} {time} - {weights}\n"
    return res
