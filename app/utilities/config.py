from pydantic_settings import BaseSettings
# from fastapi_mail import ConnectionConfig

class Settings(BaseSettings):
    DB_PORT : int
    DB_USER : str
    DB_NAME : str
    DB_PASSWORD : str
    DB_HOST : str

    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    REFRESH_TOKEN_EXPIRE_DAYS : int

    SUPERADMIN_TITLE : str
    SUPERADMIN_FIRST_NAME: str
    SUPERADMIN_LAST_NAME: str
    SUPERADMIN_EMAIL: str
    SUPERADMIN_PASSWORD: str

    LIMIT : int

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"

settings = Settings()