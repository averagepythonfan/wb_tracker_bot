import sqlite3 as sq
from contextlib import asynccontextmanager, contextmanager
from config import DATABASE

@asynccontextmanager
async def transaction(db_name : str = DATABASE):
    conn = sq.connect(db_name)
    cur = conn.cursor()
    yield cur
    conn.commit()
    conn.close()

@contextmanager
async def transaction_sync(db_name : str = DATABASE):
    conn = sq.connect(db_name)
    cur = conn.cursor()
    yield cur
    conn.commit()
    conn.close()