from django.apps import AppConfig
import os
import redis
from redis.client import PubSub

class MainPageConfig(AppConfig):
    name = 'main_page'
    redis_client: redis.Redis | None = None
    pubsub: PubSub = None

    def ready(self):
        MainPageConfig.redis_client = redis.client.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
        )
        MainPageConfig.pubsub = MainPageConfig.redis_client.pubsub()
        MainPageConfig.pubsub.subscribe('service_answer')


