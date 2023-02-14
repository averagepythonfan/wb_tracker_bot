import time
import random
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from sqdb import conn, cur

#set options for webdriver
options = Options()
options.add_argument("-headless")

while True:
    with webdriver.Remote(options=options) as driver:
        for el in cur.execute('SELECT article, userid FROM products;'):
            url = f'https://www.wildberries.ru/catalog/{el[0]}/detail.aspx'
            driver.get(url)
            time.sleep(2)

            catch = re.findall(r'<ins class="price-block__final-price">.*?</ins>', driver.page_source)[0]
            final_price = catch.replace(' ', '').replace('&nbsp;','')[37:-7]
            wb_search_title = driver.find_element(By.CLASS_NAME, "product-page__header")

            couple = (wb_search_title.text.replace('\n', ' '), int(final_price))
            # print(couple)
            time.sleep(random.randrange(4, 10))
            cur.execute(f'''
                INSERT INTO tracker ( article, name, price, userid, data )
                    VALUES ( {el[0]}, '{couple[0]}', {couple[1]}, {el[1]}, {int(time.time())});
            ''')
            conn.commit()
    time.sleep(random.randrange(3600, 4800))