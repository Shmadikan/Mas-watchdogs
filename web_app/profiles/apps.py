from django.apps import AppConfig
import os
import redis

class ProfilesConfig(AppConfig):
    name = 'profiles'
    redis_client: redis.Redis | None = None

    def ready(self):
        ProfilesConfig.redis_client = redis.client.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
        )
