import redis.asyncio as redis
import asyncio
import json


class RedisAnalyzator:

    def __init__(self, channels):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )

        self.channels: list[str] = channels
        self.pubsub = self.client.pubsub()

    @classmethod
    async def create_connection(cls, channels) -> 'RedisAnalyzator':
        instance = RedisAnalyzator(channels)

        await instance.pubsub.subscribe(channels[0])
        instance.iterator = instance.pubsub.listen()
        return instance



    async def get_data_from_agent(self) -> dict[str,dict] | None:
        async for mg in self.iterator:
            if mg["type"] == "message":
               json_data:dict[str, dict] = json.loads(mg["data"])
               return json_data

    async def send_data_to_coordinator(self, data_json: dict):
        print("Send data to coordinator...")
        data_json = json.dumps(data_json)
        await self.client.publish(channel="analyze-coordinator", message=data_json)