import redis.asyncio as redis
import asyncio
import json


class RedisAuditor:
    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )
        self.coordinator_channel = "coordinatorSend"
        self.external_channel = "externalReceive"
        self.pubsub = self.client.pubsub()
        self.iterator = None

    @classmethod
    async def create_connection(cls):
        instance = RedisAuditor()
        await instance.pubsub.subscribe(instance.external_channel)
        instance.iterator = instance.pubsub.listen()
        return instance

    async def data_from_external_source(self) -> list[str] | None:
        async for message in self.iterator:
            if message["type"] == "message":
               json_data: list[str] = json.loads(message["data"])

               return json_data


    async def send_data_to_coordinator(self, message):
        await self.client.publish(self.coordinator_channel, json.dumps(message))