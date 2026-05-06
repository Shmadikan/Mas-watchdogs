import asyncio
from concurrent.futures import ThreadPoolExecutor
from asyncio import AbstractEventLoop
from RedisAnalyzator import RedisAnalyzator
from ScannersStrategy import *
from ScannersStrategy.SearchSplotScannerStrategy import SearchSplotScannerStrategy


def instructions_for_agent_execute(instructions:tuple[str, dict]):
    """Исполнение в потоке какого то из сканеров (пока два пусть)"""
    print(instructions)
    scanner_name = instructions[1]["scanner"]
    scanner: AbstractScannerStrategy | None = None
    if scanner_name == "nmap":
       scanner = NmapScannerStrategy(instructions)
    elif scanner_name == "nuclei":
       scanner = NucleiScannerStrategy(instructions)
    elif scanner_name == "searchsplot":
       scanner = SearchSplotScannerStrategy(instructions)
    else:
       scanner = NmapScannerStrategy(instructions)

    result = scanner.execute()
    print(result)



async def run_analyzer_flow(instructions_for_agent: tuple[str, dict], loop: AbstractEventLoop, executor):
    result = await loop.run_in_executor(executor, instructions_for_agent_execute, instructions_for_agent)

    # Redis отправка

async def main():
    loop: AbstractEventLoop = asyncio.get_event_loop()
    RedisConnection = RedisAnalyzator()
    task_redis = asyncio.create_task(RedisConnection.get_data_from_agent())
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(2):
            ip_targets: dict[str, dict] = await task_redis
            for i in ip_targets.items():
                asyncio.create_task(run_analyzer_flow(i, loop, executor))
            await asyncio.sleep(5)




asyncio.run(main())









