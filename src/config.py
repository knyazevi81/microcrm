from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    SECRET_KEY: str
    ALG: str

    ROOT_EMAIL: str
    ROOT_USERNAME: str
    ROOT_PASSWORD: str

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_USER: str
    REDIS_USER_PASSWORD: str

    @property
    def redis_url(self):
        if self.REDIS_PASSWORD:
            return f"redis://{self.REDIS_USER}:{self.REDIS_USER_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        else:
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @property
    def DATABASE_URL(
        self,
    ) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()  # type: ignore
