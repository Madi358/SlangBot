from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    admin_username: str


@dataclass
class Services:
    openrouter_api_key: str
    yandex_api_key: str
    yandex_folder_id: str


@dataclass
class Settings:
    bots: Bots
    services: Services


def get_settings(path: str = ".env"):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN_API"),
            admin_id=env.int("ADMIN_ID"),
            admin_username=env.str("ADMIN_USERNAME")
        ),
        services=Services(
            openrouter_api_key=env.str("OPENROUTER_API_KEY"),
            yandex_api_key=env.str("YANDEX_API_KEY"),
            yandex_folder_id=env.str("YANDEX_FOLDER_ID")
        )
    )


settings = get_settings()
