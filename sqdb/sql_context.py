import sqlite3 as sq
from contextlib import asynccontextmanager
from config import DATABASE

@asynccontextmanager
async def transaction(db_name : str = DATABASE):
    conn = sq.connect(db_name)
    cur = conn.cursor()
    yield cur
    conn.commit()
    conn.close()