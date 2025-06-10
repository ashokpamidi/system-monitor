import asyncio

from monitor import initiate_make_observation
from db_operations import check_if_table_exists, initiate_clear_buffer, housekeeping

async def main():
    check_if_table_exists()
    housekeeping()
    observation_task = asyncio.create_task(initiate_make_observation())
    buffer_task = asyncio.create_task(initiate_clear_buffer())
    
    await asyncio.gather(observation_task, buffer_task)

if __name__ == '__main__':
    asyncio.run(main())