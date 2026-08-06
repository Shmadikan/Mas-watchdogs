from django.apps import AppConfig
import redis
from redis.client import PubSub

class MainPageConfig(AppConfig):
    name = 'main_page'
    redis_client = None
    pubsub: PubSub = None

    def ready(self):
        MainPageConfig.redis_client = redis.client.Redis()
        MainPageConfig.pubsub = MainPageConfig.redis_client.pubsub()
        MainPageConfig.pubsub.subscribe('service_answer')


