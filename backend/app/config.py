from pydantic import computed_field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1000

    POSTGRES_DEV_SERVER: str
    POSTGRES_DEV_PORT: int = 5432
    POSTGRES_DEV_USER: str
    POSTGRES_DEV_PASSWORD: str = ""
    POSTGRES_DEV_DB: str

    @computed_field
    @property
    def DB_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_DEV_USER,
            password=self.POSTGRES_DEV_PASSWORD,
            host=self.POSTGRES_DEV_SERVER,
            port=self.POSTGRES_DEV_PORT,
            path=self.POSTGRES_DEV_DB,
        )


settings = Settings()  # type: ignore
