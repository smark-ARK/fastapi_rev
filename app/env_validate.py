from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXPIRE_MINUTES: int
    ACCESS_KEY_ID: str
    SECRET_ACCESS_KEY: str


settings = Settings(_env_file=".env")
