import asyncio

import uvicorn
from server.monitor import make_observation
from server.db_operations import check_if_table_exists, housekeeping, write_to_db
from server.config import QUEUE_LEN, OBSERVATION_INTERVAL
from server.cache_queue import CacheQueue
from server.api import set_queue, app

#initiate cache queue
cache_q = CacheQueue()

async def write_to_cache(q, obs):
    if q.size > QUEUE_LEN:
        q.dequeue()
    print(f"len of queue: {q.size}")
    q.enqueue(obs)

async def initiate_make_observation():
    while True:
        observation = make_observation()
        await write_to_cache(cache_q, observation)
        await asyncio.sleep(OBSERVATION_INTERVAL)

async def initiate_write_to_db():
    check_if_table_exists()
    housekeeping()
    while True:
        write_to_db(cache_q)
        await asyncio.sleep(QUEUE_LEN)   

async def main():
    observation_task = asyncio.create_task(initiate_make_observation())
    write_to_db_task = asyncio.create_task(initiate_write_to_db())
    set_queue(cache_q)

    api_config = uvicorn.Config(app, host = "0.0.0.0", port=8000)
    server = uvicorn.Server(api_config)
    api_server_task = asyncio.create_task(server.serve())

    await asyncio.gather(observation_task, write_to_db_task, api_server_task)

if __name__ == '__main__':
    asyncio.run(main())