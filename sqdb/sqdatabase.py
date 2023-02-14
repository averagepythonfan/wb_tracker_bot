import sqlite3 as sq


def connect_to_db():
    global conn, cur
    conn = sq.connect('wb.db')
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
        name TEXT,
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

async def fetch_articles(user_id : int) -> list:
    res = cur.execute('SELECT article FROM products;')
    return res.fetchall()

async def insert_user(userid : int, username : str, status : str = 'free'):
    cur.execute(f"INSERT INTO users ( userid, username, status) VALUES ( {userid}, '{username}', '{status}')")
    conn.commit()

async def insert_track(article : int, name : str, price : int, userid : int, data : int):
    cur.execute(f'''
        INSERT INTO tracker VALUES ( {article}, '{name}', {price}, {userid}, {data})
    ''')
    conn.commit()

async def select_last_two_rows(article : int):
    res = cur.execute(f'''
        SELECT * FROM tracker
        WHERE article = {article}
        ORDER BY data DESC
        LIMIT 2;
    ''')
    return res.fetchall()