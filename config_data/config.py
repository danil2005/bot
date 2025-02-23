from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class DataBase:
    host: str  # хост, на котором работает MySQL
    user: str  # ваше имя пользователя
    password: str  # ваш пароль
    name_db: str  # название базы данных


@dataclass
class Config:
    tg_bot: TgBot
    type_db: str
    data_base: DataBase


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        data_base=DataBase(
            host=env("HOST_DB"),
            user=env("USER_DB"),
            password=env("PASSWORD_DB"),
            name_db=env("NAME_DB"),
        ),
        type_db=env("TYPE_DB"),
    )


config: Config = load_config()
