import asyncio

from core.monitor import make_observation
from core.db_operations import check_if_table_exists, housekeeping, save_to_buffer, clear_buffer 
from core.Queue import Queue

cache_q: Queue = Queue()

OBSERVATION_INTERVAL = 1
MAX_BUFFER_LEN = 10

async def initiate_make_observation():
    while True:
        observation = make_observation()
        save_to_buffer(cache_q, observation)
        await asyncio.sleep(OBSERVATION_INTERVAL)

async def initiate_clear_buffer():
    while True:
        clear_buffer(cache_q)
        await asyncio.sleep(MAX_BUFFER_LEN)   

async def main():
    check_if_table_exists()
    housekeeping()
    observation_task = asyncio.create_task(initiate_make_observation())
    buffer_task = asyncio.create_task(initiate_clear_buffer())
    
    await asyncio.gather(observation_task, buffer_task)

if __name__ == '__main__':
    asyncio.run(main())