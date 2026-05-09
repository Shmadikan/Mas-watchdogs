import redis.asyncio as redis
import asyncio
import json


class RedisCoordinator:
    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )
        self.analyze_send_channel = "coordinator-analyze"
        self.auditor_receive_channel = "auditor-coordinator"
        self.analyze_receive_channel = "analyze-coordinator"
        self.queue_analyze = asyncio.Queue()
        self.queue_auditor = asyncio.Queue()
        self.pubsub = self.client.pubsub()
        self.iterator = None

    @classmethod
    async def create_connection(cls):
        instance = RedisCoordinator()
        await instance.pubsub.subscribe(instance.analyze_receive_channel)
        await instance.pubsub.subscribe(instance.auditor_receive_channel)
        instance.iterator = instance.pubsub.listen()
        return instance


    async def get_data(self):
        async for msg in self.iterator:
            if msg["type"] == "message":
               print("hey, got message!!!! from", msg["channel"])
               if msg["channel"] == self.auditor_receive_channel:
                  await self.queue_auditor.put(json.loads(msg["data"]))

               if msg["channel"] == self.analyze_receive_channel:
                  print("I think i dont have data:", msg["data"])
                  await self.queue_analyze.put(json.loads(msg["data"]))


    async def send_to_analizator(self, data: dict[str, dict]):
        await self.client.publish(self.analyze_send_channel, json.dumps(data))


