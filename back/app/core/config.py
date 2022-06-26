from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_algorithm: str = "HS256"
    access_expiration: int = 36000
    refresh_expiration: int = 72000
    access_cookie_name: str = "access_token"
    refresh_cookie_name: str = "refresh_token"
    debug: bool = False
    login_ratelimit: int = 60
    email_confirmation_timeout: int = 1800
    email_confirmation_max: int = 2
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_host: str = ""
    smtp_tls: bool = True
    smtp_url: str = ""
    password_reset_timeout: int = 1800
    password_reset_max: int = 2
    password_reset_lifetime: int = 7200
    username_min_length: int = 3
    username_max_length: int = 20
    password_min_length: int = 6
    password_max_length: int = 32
    time_delta: int = 3

    class Config:
        env_file = ".env.sample"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings


settings = get_settings()
