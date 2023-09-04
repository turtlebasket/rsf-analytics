from os import getenv
import logging
from dotenv import load_dotenv
from typing import List

initialized = False

env_vars: List[str] = """
API_URL
SPACE_ID
API_TOKEN
ADMIN_KEY
""".strip().split("\n")


def init():
    if getenv("LOCAL_ENV"):
        load_dotenv()

    for k in env_vars:
        if not getenv(k):
            logging.error(f"Missing environment variable: {k}")
            exit(1)

    global initialized
    initialized = True


def get(key: str) -> str:
    global initialized
    if not initialized:
        init()
    return str(getenv(key))
