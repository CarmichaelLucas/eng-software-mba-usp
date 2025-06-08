from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///database.db'
    auth_base_url: str

    model_config = SettingsConfigDict(env_file='.env')
