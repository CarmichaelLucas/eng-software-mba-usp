from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///database.db'
    secret_key: str = 'segredo_supersecreto'

    model_config = SettingsConfigDict(env_file='.env')
