from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = ...  # ENVIRONMENT Parameter
    SECRET_KEY: str = ... # ENVIRONMENT Parameter
    ALGORITHM: str = ... # ENVIRONMENT Parameter
    CELERY_URL: str = ... # ENVIRONMENT Param
    ACCESS_TOKEN_LIFETIME: int = 30
    REFRESH_TOKEN_LIFETIME: int = 1

    class Config:
        env_file = '.env'


settings = Settings()