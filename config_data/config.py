from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class TgBot:
    token: str


@dataclass
class DataBase:
    host: str
    port: int
    user: str
    password: str
    name_db: str


@dataclass
class Redis:
    host: str  
    port: int  


@dataclass
class Config:
    tg_bot: TgBot
    type_db: str
    data_base: DataBase
    redis: Redis


def load_config(path: str | None = None) -> Config:

    load_dotenv(dotenv_path=path)

    type_db = type_db=os.getenv("TYPE_DB")

    if type_db == "mysql":
        return Config(
            tg_bot=TgBot(token=os.getenv("BOT_TOKEN")),
            data_base=DataBase(
                host=os.getenv("HOST_DB"),
                port=int(os.getenv("PORT_DB")),
                user=os.getenv("USER_DB"),
                password=os.getenv("PASSWORD_DB"),
                name_db=os.getenv("NAME_DB"),
            ),
            type_db=type_db,
            redis=Redis(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT"))
            )
        )
    elif type_db == "sqllite":
         return Config(
            tg_bot=TgBot(token=os.getenv("BOT_TOKEN")),
            type_db=type_db,
        )



config: Config = load_config()
