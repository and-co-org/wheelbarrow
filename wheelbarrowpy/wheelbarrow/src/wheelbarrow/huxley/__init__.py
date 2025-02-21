from rich import print
import numpy as np
import time
from dotenv import load_dotenv
import os
from pathlib import Path

"""
this is huxley's file for wheelbarrow
which contains my personal utils!
"""

def hello() -> str:
    return "Hello from wheelbarrow.huxley!"


def alert(message, at=True):
    import requests
    webhook_url = "https://discord.com/api/webhooks/1342398467976200233/wc_l8MCnZWmNL0xj6calNsI1KulQ8uQsybi-_4_f2frJnj1qv27tfFH9BbD1qvOaT4hZ"

    if at:
        cur = Path(__file__).parent
        env_path = cur / "../../../../../.env"
        load_dotenv(env_path)

        message = f"<@{os.getenv('HUXLEY_DISCORD_USER_ID')}> {message}"

    requests.post(
            webhook_url,
            json={"content": message}
        )


####################
#    DECORATORS    #
####################
def timeit(precision=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = round(end_time - start_time, precision)
            print(f"{func.__name__} took {duration}s")
            return result
        return wrapper
    return decorator

