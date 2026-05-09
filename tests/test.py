# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-72aa87a91e404dcbb59e96cf8c9eb7ea",
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": """Ты агент в мультиагентной системе по анализу уязвимости в сети. 
        Ты получаешь данные от агента аудитора в формате JSON, твоя задача сгенерировать, на основании присланной информации какую то краткую характеристику сети"""},
        {"role": "user", "content": "[[\\\"172.17.0.1\\\", 8000, {\\\"proto\\\": \\\"tcp\\\", \\\"service\\\": \\\"http-alt\\\", \\\"version\\\": \\\"\\\"}], [\\\"172.17.0.2\\\", 8000, {\\\"proto\\\": \\\"tcp\\\", \\\"service\\\": \\\"nagios-nsca\\\", \\\"version\\\": \\\"Nagios NSCA\\\"}"},
    ],
    stream=False,
    reasoning_effort="low",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)