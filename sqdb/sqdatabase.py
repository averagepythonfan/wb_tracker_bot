import sqlite3 as sq
from config import DATABASE

def connect_to_db():
    global conn, cur
    conn = sq.connect(DATABASE)
    cur = conn.cursor()

    try:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users
        (userid INTEGER NOT NULL,
        username TEXT NOT NULL PRIMARY KEY,
        status TEXT NOT NULL
        );''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS products
        (article INTEGER NOT NULL,
        userid INTEGER NOT NULL
        );''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS tracker
        (article INTEGER NOT NULL,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        userid INTEGER NOT NULL,
        data INTEGER NOT NULL
        );''')

        conn.commit()

    except sq.Error as error:
        print(f'Error {error}')

async def fetch_products(userid : int) -> list:
    res = cur.execute(f'SELECT article, name, price FROM tracker WHERE userid = {userid};')
    return res.fetchall()

async def insert_user(userid : int, username : str, status : str = 'free') -> None:
    cur.execute(f"INSERT INTO users ( userid, username, status) VALUES ( {userid}, '{username}', '{status}');")
    conn.commit()

async def check_products_count(userid : int) -> int:
    res = cur.execute(f'''
    SELECT article FROM products
    WHERE userid = {userid};
    ''')
    return len(res.fetchall())

async def check_product_exist(article : int, userid : int) -> int:
    res = cur.execute(f'''
    SELECT article FROM products
    WHERE article = {article} AND userid = {userid};
    ''')
    return len(res.fetchall())


async def check_status(userid : int) -> list:
    res = cur.execute(f'SELECT status FROM users WHERE userid = {userid}')
    return res.fetchall()

async def insert_product(article : int, userid : int) -> None:
    cur.execute(f'''
        INSERT INTO products VALUES ( {article}, {userid});
    ''')
    conn.commit()

async def delete_product(article : int, userid : int) -> None:
    cur.execute(f'DELETE FROM products WHERE article = {article} AND userid = {userid};')
    conn.commit()

async def insert_track(article : int, name : str, price : int, userid : int, data : int) -> None:
    cur.execute(f'''
        INSERT INTO tracker VALUES ( {article}, '{name}', {price}, {userid}, {data});
    ''')
    conn.commit()

async def select_last_two_rows(article : int) -> list:
    res = cur.execute(f'''
        SELECT * FROM tracker
        WHERE article = {article}
        ORDER BY data DESC
        LIMIT 2;
    ''')
    return res.fetchall()