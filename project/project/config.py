from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///database.db'
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    kafka_bootstrap_servers: str
    token_validation_request_topic: str
    token_validation_response_topic: str

    model_config = SettingsConfigDict(env_file='.env')
