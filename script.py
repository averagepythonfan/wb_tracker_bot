import sqlite3 as sq
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


#set options for webdriver
options = Options()
options.add_argument("-headless")


try:
    conn = sq.connect('wb.db')
    cur = conn.cursor()
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
    print('INIT SUCCESS')

except sq.Error as error:
    print(f'Sorry, we have an error {error}')

finally:
    conn.close()


# def parse_product(article : int) -> tuple:

#     url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'
#     driver.get(url)
#     time.sleep(2)
#     catch = re.findall(r'<ins class="price-block__final-price">.*?</ins>', driver.page_source)[0]
#     final_price = catch.replace(' ', '').replace('&nbsp;','')[37:-7]
#     wb_search_title = driver.find_element(By.CLASS_NAME, "product-page__header")
#     #return wb_search_title.text + wb_search_price.text
#     couple = (wb_search_title.text.replace('\n', ' '), int(final_price))
#     print(couple)
#     time.sleep(random.randrange(4, 10))
#     driver.quit()
#     return couple

with webdriver.Remote(options=options) as driver:
    while True:
        break

        cur.execute('FROM pruducts SELECT article;')
        res = cur.fetchall()