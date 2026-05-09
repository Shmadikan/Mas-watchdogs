import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from asyncio import AbstractEventLoop
from RedisAnalyzator import RedisAnalyzator
from ScannersStrategy import *
from ScannersStrategy.SearchSplotScannerStrategy import SearchSplotScannerStrategy


def instructions_for_agent_execute(instructions:tuple[str, dict]):
    """Исполнение в потоке какого то из сканеров (пока три пусть, но расширяемо через стратегии)"""
    print(instructions)
    scanner_name = instructions[1].get("scanner", "nmap")
    scanner: AbstractScannerStrategy | None = None
    if scanner_name == "nmap":
       scanner = NmapScannerStrategy(instructions)
    elif scanner_name == "nuclei":
       scanner = NucleiScannerStrategy(instructions)
    elif scanner_name == "searchsplot":
       scanner = SearchSplotScannerStrategy(instructions)

    result = scanner.execute()
    return result




async def run_analyzer_flow(instructions_for_agent: tuple[str, dict], loop: AbstractEventLoop, executor, redis_connector):
    result = await loop.run_in_executor(executor, instructions_for_agent_execute, instructions_for_agent)
    print(result)
    return result

async def collect_all_info(tasks, redis_connector):
    results = []

    for ready in asyncio.as_completed(tasks):
        print("task ready one")
        results.extend(await ready)
    asyncio.create_task(redis_connector.send_data_to_coordinator(results))



async def main():
    loop: AbstractEventLoop = asyncio.get_event_loop()

    RedisConnection = await RedisAnalyzator.create_connection(["coordinator-analyze", "analyze-coordinator"])


    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            print("Start")
            task_redis = asyncio.create_task(RedisConnection.get_data_from_agent())
            ip_targets: dict[str, dict] = await task_redis
            tasks = []
            for i in ip_targets.items():
                tasks.append(asyncio.create_task(run_analyzer_flow(i, loop, executor, RedisConnection)))
            asyncio.create_task(collect_all_info(tasks, RedisConnection))

asyncio.run(main())









