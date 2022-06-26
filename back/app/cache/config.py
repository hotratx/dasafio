import aioredis
from app.cache.redis import RedisBackend

# from pydantic import BaseSettings, Field


# class Settings(BaseSettings):
#     REDIS_HOST: str
#     REDIS_PORT: str

#     class config:
#         case_sensitive = True

# settings = Settings()


# redis = RedisBackend()
# redis._redis = aioredis.from_url(settings.REDIS_HOST +"://"+ settings.REDIS_HOST+":"+settings.REDIS_PORT)

