import asyncio
from concurrent.futures import ThreadPoolExecutor
from asyncio import AbstractEventLoop
from RedisAnalyzator import RedisAnalyzator
from .ScannersStrategy import *


def instructions_for_agent_execute(instructions:dict):
    """Исполнение в потоке какого то из сканеров (пока два пусть)"""
    scanner: AbstractScannerStrategy = NmapScannerStrategy()
    if instructions["instrument"] == "Nuclei":
       scanner = NucleiScannerStrategy()
    elif instructions["instrument"] == "":




async def run_analyzer_flow(instructions_for_agent: dict, loop: AbstractEventLoop, executor):
    result = await loop.run_in_executor(executor, instructions_for_agent_execute, instructions_for_agent)

    # Redis отправка

async def main():
    loop: AbstractEventLoop = asyncio.get_event_loop()
    RedisConnection = RedisAnalyzator()
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            instructions_for_agent = await RedisConnection.get_data_from_agent()
            asyncio.create_task(run_analyzer_flow(instructions_for_agent, loop))
"""Переписать в соответствии с новым JSON"""





asyncio.run(main())


