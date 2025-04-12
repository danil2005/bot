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


async def main():
    """Функция конфигурирования и запуска бота"""
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    await check_db()

    bot = Bot(token=config.tg_bot.token)
    
    redis = Redis(host=config.redis.host, port=config.redis.port)
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(questionnaire_handlers.router)
    dp.include_router(edit_workouts_handlers.router)
    dp.include_router(workouts_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())