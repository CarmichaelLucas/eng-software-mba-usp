from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///database.db'
    kafka_bootstrap_servers: str
    token_validation_request_topic: str
    token_validation_response_topic: str
    todo_dlq_topic: str

    model_config = SettingsConfigDict(env_file='.env')
