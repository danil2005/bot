import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import (
    other_handlers,
    questionnaire_handlers,
    workouts_handlers,
    edit_workouts_handlers,
)
from keyboards.main_menu import set_main_menu
from aiogram_sqlite_storage.sqlitestore import SQLStorage

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    storage = SQLStorage("my_db_path.db", serializing_method="pickle")
    dp = Dispatcher(storage=storage)

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(questionnaire_handlers.router)
    dp.include_router(edit_workouts_handlers.router)
    dp.include_router(workouts_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
