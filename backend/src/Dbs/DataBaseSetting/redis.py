import redis.asyncio as redis
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_POST")

logging.info(f"Using host: {host}")
logging.info(f"Using port Key: {port}")

JTI_EXPIERY = 3600
token_blocklist = redis.from_url(f"redis://{host}:{port}", decode_responses=True)

async def add_jit_to_blocklist(jti:str) -> None:
    await token_blocklist.set(name=jti , value ="", ex=JTI_EXPIERY)


async def get_jit_to_blocklist(jti:str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None