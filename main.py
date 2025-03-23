import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import config
from handlers import (
    other_handlers,
    questionnaire_handlers,
    workouts_handlers,
    edit_workouts_handlers,
)
from keyboards.keyboards import set_main_menu

from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from database.database import check_db

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

    # Проверяем базу данных асинхронно
    await check_db()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    
    redis = Redis(host="localhost")
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(questionnaire_handlers.router)
    dp.include_router(edit_workouts_handlers.router)
    dp.include_router(workouts_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())