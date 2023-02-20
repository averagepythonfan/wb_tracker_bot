from sqlalchemy import URL, create_engine
from contextlib import asynccontextmanager, contextmanager
from config import DATABASE, DRIVERNAME, USERNAME, PASSWORD, PORT, HOST


params = {
    "drivername": DRIVERNAME,
    "username": USERNAME,
    "password": PASSWORD,
    "host": HOST,
    "port": PORT,
    "database": DATABASE
}

url_object = URL.create(**params)
engine = create_engine(url_object)

@asynccontextmanager
async def transaction():
    conn = engine.connect()
    yield conn
    conn.commit()
    conn.close()

@contextmanager
def transaction_sync():
    conn = engine.connect()
    yield conn
    conn.commit()
    conn.close()
