import asyncio

from monitor import make_observation, save_to_buffer
from db_operations import check_if_table_exists, housekeeping, clear_buffer 

MAX_BUFFER_LEN = 20

async def initiate_make_observation():
    while True:
        observation = make_observation()
        save_to_buffer(observation)
        await asyncio.sleep(1)

async def initiate_clear_buffer():
    while True:
        clear_buffer()
        await asyncio.sleep(MAX_BUFFER_LEN)   

async def main():
    check_if_table_exists()
    housekeeping()
    observation_task = asyncio.create_task(initiate_make_observation())
    buffer_task = asyncio.create_task(initiate_clear_buffer())
    
    await asyncio.gather(observation_task, buffer_task)

if __name__ == '__main__':
    asyncio.run(main())