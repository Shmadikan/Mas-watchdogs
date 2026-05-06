#import redis.asyncio as redis
import asyncio


class RedisAnalyzator:

    def __init__(self):
        pass

    async def get_data_from_agent(self) -> dict[str,dict]:
        await asyncio.sleep(1)
        return {
            "172.17.0.3": {
                "ports": {
                    "80": {"scripts": ["check_sql_injection", "check_xss"]},
                    "3306": {"scripts": ["check_mysql_empty_password"]},
                    "443": {"scripts": ["check_heartbleed"]}
                },
                "global_scripts": ["check_os"],
                "scanner": "nmap",
                "ping": False,
                "scan_speed": "normal",
                "intensity": "deep"
            }
        }


