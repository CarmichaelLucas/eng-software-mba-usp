from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///database.db'
    auth_base_url: str
    kafka_bootstrap_servers: str
    token_validation_request_topic: str
    token_validation_response_topic: str

    model_config = SettingsConfigDict(env_file='.env')
