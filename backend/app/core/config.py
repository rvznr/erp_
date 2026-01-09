import os
from functools import lru_cache


class Settings:
    PROJECT_NAME: str = "Kucukler Insaat ERP"
    API_V1_STR: str = "/api"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME_SUPER_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "erp_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "erp_pass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "erp_db")

    FILE_STORAGE_PATH: str = os.getenv("FILE_STORAGE_PATH", "/data/files")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


