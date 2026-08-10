import asyncio
import pdb

from openai import OpenAI
import json
import keyring
import pprint
from RedisCoordinator import RedisCoordinator

api_key = keyring.get_password('app', 'api_key')
base_url = keyring.get_password('app', 'model_url')

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


with open("PROMPT.md", "r") as file:
    SYSTEM_PROMPT = file.read()

messages = [
    {"role":"system", "content":SYSTEM_PROMPT}
]

scanned_vul = []

async def get_settings(redis_client: RedisCoordinator, client: OpenAI):
    while True:
        print(client.base_url, client.api_key)
        data: dict = await redis_client.queue_settings.get()
        keyring.set_password('app', 'api_key', data['api-key'])
        keyring.set_password('app', 'model_url', data['model-url'])
        keyring.set_password('app', 'model', data['model'])
        client.base_url = data['model-url']
        client.api_key = data['api-key']

        print(client.base_url, client.api_key)



async def get_data_from_analyze(redis_client: RedisCoordinator, id):
    print("get data from analyze")
    data: list[dict] = await redis_client.queue_analyze.get()
    print(data)
    scanned_vul.extend(data)

    report_prompt = {
        "role": "user",
        "content": (
            "Ты — эксперт по кибербезопасности. На основе предоставленных результатов "
            "сканирования уязвимостей сформируй итоговый отчёт в формате пригодном для отображения на странице сайта"
            "Отчёт должен содержать: итог: краткая сводка, findings (список "
            "найденных уязвимостей с severity и описанием), recommendations (рекомендации "
            "по устранению). Данные сканирования:\n"
            + json.dumps(scanned_vul, ensure_ascii=False)
        )
    }
    try:
        print("Generating final LLM report...")
        response = client.chat.completions.create(
            model=keyring.get_password('app', 'model'),
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, report_prompt],
            reasoning_effort="medium",
            extra_body={"thinking": {"type": "enabled"}}
        )
        report = response.choices[0].message.content

        await redis_client.send_report_to_django(report, id)
        print("Report sent to Django")
    except Exception as e:
        await redis_client.send_report_to_django(e, id)


async def send_data_to_analyze(data, redis_client, id):
    await redis_client.send_to_analizator(data)
    asyncio.create_task(get_data_from_analyze(redis_client, id))


async def main():

    inst = await RedisCoordinator.create_connection()
    asyncio.create_task(inst.get_data())
    asyncio.create_task(get_settings(inst, client))
    while True:
        answer = await inst.queue_auditor.get()
        scan, id = answer
        content_send = {"role": "user", "content": json.dumps(scan)}
        print("Send to LLM...")
        response = client.chat.completions.create(
            model=keyring.get_password('app', 'model'),
            messages=messages+[content_send],
            response_format={
                'type': 'json_object'
            },
            reasoning_effort="medium",
            extra_body={"thinking": {"type": "enabled"}}
        )
        pprint.pprint(response.choices[0].message)
        answer_parsed = json.loads(response.choices[0].message.content)
        asyncio.create_task(send_data_to_analyze(answer_parsed, inst, id))
        pprint.pprint(json.loads(response.choices[0].message.content))


asyncio.run(main())