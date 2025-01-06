from database import database

LEXICON: dict[str, str] = {
    '/start': 'Привет! Этот бот поможет вести статистику тренировок.\n'
    'Мне нужны некоторые данные о Вас.\n'
    'Вы готовы ответить на пару вопросов?',
    'enter_name': 'Введите полное имя.',
    'error_name': 'Имя должно сосоять только из букв.',
    'enter_age': 'Введите возраст.',
    'error_old': 'Возраст должен состоять только из цифр',
    'enter_gender': 'Введите пол.',
    'enter_height': 'Введите рост.',
    'error_height': 'Рост должен состоять только из цифр.',
    'enter_weight': 'Введите вес.',
    'error_weight': 'Вес должен состоять только из цифр.',
    'use_btn_pls': 'Воспользуйтесь пожалуйста кнопками снизу.',
    'wait': 'Если передумаете, просто нажмите кнопку /start.',
    'questionnaire_ready': 'Анкета готова!\nТеперь можно начать составлять программы тренировок и тренироваться.',
    'questionnaire_again': 'Тогда давайте заполним анкету заново.',
    'menu': 'Меню',
    'enter_name_workout': 'Введите название тренировки', 
    'create_workout_success': 'Тренировкка создана',
    'repeat_name_workout': 'Тренировка с таким названием уже существует.\nВведите другое название либо удалите тренировку с таким же названием.',
    'select_archive': 'Выберите тренировки для архивации',
    'delite': 'Выберите тренировки для удаления',
    'dearchive': 'Выберите тренировки для восстановления из архива',
    'workout': 'Тренировка:',
    'enter_name_exercise': 'Введите название упражнения',
    'repeat_name_exercise': 'Упражнение с таким названием уже существует.nВведите другое название.',

}

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Старт',
    '/help': 'Справка по работе бота'
}

LEXICON_BUTTON : dict[str, str] = {
    'yes': 'ДА',
    'no': 'НЕТ',
    'male': 'Мужской',
    'female': 'Женский',
}

LEXICON_MAIN_MENU : dict[str, str] = {
    'edit_workouts': 'Редактировать тренировки',
    'fix_weight': 'Зафиксировать вес'
}

LEXICON_EDIT_ACTION : dict[str, str] = {
    'ready': 'Готово'
}

LEXICON_EDIT_WORKOUTS : dict[str, str] = {
    'create_workout': 'Создать',
    'archive': 'Архивировать',
    'delite': 'Удалить',
    'dearchive': 'Добавить из архива',
    'main_menu': 'Главное меню',
}

WORKOUT_MENU: dict[str, str] = {
    'start': 'Старт',
    'watch': 'Просмотр',
    'main_menu': 'Главное меню',
}

START_WORKOUT: dict[str, str] = {
    'new': 'Новое упражнение',
    'other': 'Другое упражнение',
    'end': 'Конец тренировки',
}

DO_EXERCISE: dict[str, str] = {
    'finish': 'Закончить упражнение',
}

def weight_workout(id):
    data = database.get_weight_workout(id)
    return '\n'.join([f'{i}: {j}'for i,j in data])

def workout_type_text(type_workout: int):
    res = database.get_name_workout(type_workout) + '\n\n'
    # получаем id последних тренировок
    ids = database.get_latest_workout_ids(type_workout)
    ids.reverse()
    for i in ids:
        date = database.get_date_workout(i)
        weights = weight_workout(i)
        res += date + '\n' + weights + '\n\n'
    
    return res






