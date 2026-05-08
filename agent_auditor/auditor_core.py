import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

from RedisAuditor import RedisAuditor
import nmap
from asyncio import Queue, AbstractEventLoop
from concurrent.futures import Executor
from threading import Lock
Lock = Lock()


INTERVAL_TIME_SECONDS = 30
import pprint
queue = Queue()
scanned_nets = dict()


def ping_scan(subnet):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=subnet, arguments="-sn -T4")

    return list(scanner.all_hosts())


def parse_nmap_result(results:list | tuple) -> list[tuple]:
    res = []
    for result in results:
        for host, ports in result.items():
            for port, info in ports.items():
                res.append((host, port, info))
    return res


def subnet_thread_analyze(subnet: str) -> dict:
    scanner = nmap.PortScanner()
    scanner.scan(hosts=subnet, arguments="-sS -sV -F -T4 --privileged")

    results = {}
    for host in scanner.all_hosts():
        results[host] = {}

        for proto in scanner[host].all_protocols():
            for port in scanner[host][proto].keys():
                service = scanner[host][proto][port]
                results[host][port] = {
                    "proto": proto,
                    "service": service["name"],
                    "version": f'{service["product"]} {service["version"]}'.strip()
                }
    with Lock:
        scanned_nets[subnet] = results


    return results




async def execute_analyze_subnet(executor: Executor, redis_audit: RedisAuditor, loop: AbstractEventLoop):

    while True:
        subnets_list: list = await queue.get()
        print("start scanning...")
        tasks = []
        for net in subnets_list:
            tasks.append(loop.run_in_executor(executor, subnet_thread_analyze, net))

        results = await asyncio.gather(*tasks)
        tuples_result = parse_nmap_result(results)

        await redis_audit.send_data_to_coordinator(json.dumps(tuples_result))




async def analyze_subnet_timer(executor: Executor, loop: AbstractEventLoop, redis_audit: RedisAuditor):
    await asyncio.sleep(INTERVAL_TIME_SECONDS)
    data_send = []
    print("start planning analyze of all subnets...")
    for subnet in scanned_nets:
        if len(ping_scan(subnet)) != len(scanned_nets[subnet]):
           result = await loop.run_in_executor(executor, subnet_thread_analyze, subnet)
           tuple_parameters:list[tuple] = parse_nmap_result([result])
           data_send.extend(tuple_parameters)


    if len(data_send) != 0:
        await redis_audit.send_data_to_coordinator(json.dumps(data_send))

    asyncio.create_task(analyze_subnet_timer(executor, loop, redis_audit))



async def main():

    redis_audit = await RedisAuditor.create_connection()

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=10) as executor:
        asyncio.create_task(analyze_subnet_timer(executor, loop, redis_audit))
        asyncio.create_task(execute_analyze_subnet(executor, redis_audit, loop))
        while True:
            task = asyncio.create_task(redis_audit.data_from_external_source())
            subnets:list[str] = await task
            await queue.put(subnets)


asyncio.run(main())