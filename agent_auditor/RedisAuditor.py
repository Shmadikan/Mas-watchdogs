import redis.asyncio as redis
import json
import os

class RedisAuditor:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=0,
            decode_responses=True
        )
        self.coordinator_channel = "auditor-coordinator"
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
        'format: [172.17.0.4/24]'
        async for message in self.iterator:
            if message["type"] == "message":
               json_data: list[str] = json.loads(message["data"])

               return json_data


    async def send_data_to_coordinator(self, message):

        await self.client.publish(self.coordinator_channel, json.dumps(message))