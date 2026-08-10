from django.apps import AppConfig
import redis

class ProfilesConfig(AppConfig):
    name = 'profiles'
    redis_client: redis.Redis | None = None

    def ready(self):
        ProfilesConfig.redis_client = redis.client.Redis()
