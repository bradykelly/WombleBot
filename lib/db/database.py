import asyncio
import asyncpg


class Database:

    pool = None

    def __init__(self, bot, dsn):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.init_instance(dsn))

    async def init_instance(self, dsn):
        Database.pool = await asyncpg.create_pool(dsn)    

    async def field(self, sql, *values):
        async with Database.pool.acquire() as conn:
            return await conn.fetchval(sql, *values)
        
    async def record(self, sql, *values):
        async with Database.pool.acquire() as conn:
            return await conn.fetchrow(sql, *values)

    async def records(self, sql, *values):
        async with Database.pool.acquire() as conn:
            return await conn.fetch(sql, *values)

    async def column(self, sql, *values):
        async with Database.pool.acquire() as conn:
            rows = await conn.fetch(sql, *values)
            return [row[0] for row in rows]

    async def execute(self, sql, *values):
        async with Database.pool.acquire() as conn:
            await conn.execute(sql, *values)
            await conn.commit()

    async def executemany(self, sql, valueset):
        async with Database.pool.acquire() as conn:
            await conn.executemany(sql, valueset)
            await conn.commit()
