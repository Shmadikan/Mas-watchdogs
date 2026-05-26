import asyncio
from openai import OpenAI
import json
import pprint

client = OpenAI(
    api_key="OWN",
    base_url="https://api.deepseek.com"
)




from RedisCoordinator import RedisCoordinator
with open("PROMPT.md", "r") as file:
    SYSTEM_PROMPT = file.read()

messages = [
    {"role":"system", "content":SYSTEM_PROMPT}
]

scanned_vul = []


async def send_data_to_api(redis_client):
    pass


async def get_data_from_analyze(redis_client: RedisCoordinator):
    print("get data from analyze")
    data: list[dict] = await redis_client.queue_analyze.get()
    print(data)
    scanned_vul.extend(data)

    report_prompt = {
        "role": "user",
        "content": (
            "Ты — эксперт по кибербезопасности. На основе предоставленных результатов "
            "сканирования уязвимостей сформируй итоговый отчёт в формате JSON. "
            "Отчёт должен содержать: summary (краткая сводка), findings (список "
            "найденных уязвимостей с severity и описанием), recommendations (рекомендации "
            "по устранению). Данные сканирования:\n"
            + json.dumps(scanned_vul, ensure_ascii=False)
        )
    }
    print("Generating final LLM report...")
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, report_prompt],
        response_format={'type': 'json_object'},
        reasoning_effort="medium",
        extra_body={"thinking": {"type": "enabled"}}
    )
    report = json.loads(response.choices[0].message.content)
    pprint.pprint(report)

    await redis_client.send_report_to_django(report)
    print("Report sent to Django")


async def send_data_to_analyze(data, redis_client):
    await redis_client.send_to_analizator(data)
    asyncio.create_task(get_data_from_analyze(redis_client))


async def main():

    inst = await RedisCoordinator.create_connection()
    asyncio.create_task(send_data_to_api(inst))
    asyncio.create_task(inst.get_data())
    while True:
        answer = await inst.queue_auditor.get()
        content_send = {"role":"user", "content": json.dumps(answer)}
        print("Send to LLM...")
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages+[content_send],
            response_format={
                'type': 'json_object'
            },
            reasoning_effort="medium",
            extra_body={"thinking": {"type": "enabled"}}
        )
        pprint.pprint(response.choices[0].message)
        answer_parsed = json.loads(response.choices[0].message.content)
        asyncio.create_task(send_data_to_analyze(answer_parsed, inst))
        pprint.pprint(json.loads(response.choices[0].message.content))


asyncio.run(main())