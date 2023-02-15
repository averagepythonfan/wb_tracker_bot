import time
import random
import re
import sqlite3 as sq
import logging
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from sqdb import transaction_sync

#set logger
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


#set options for webdriver
options = Options()
options.add_argument("-headless")


#infinite update
while True:
    with webdriver.Remote(options=options) as driver:
        #products = cur.execute('SELECT * FROM products;').fetchall()
        with transaction_sync() as cur:
            products = cur.execute('SELECT * FROM products;').fetchall()
        logger.debug(f'Fetched pairs. Lenght : {len(products)}')
        for el in products:
            logger.debug(f'Start parsing for {el}')
            driver.get(f'https://www.wildberries.ru/catalog/{el[0]}/detail.aspx')

            time.sleep(2)

            try:
                catch = re.findall(r'<ins class="price-block__final-price">.*?</ins>', driver.page_source)[0]
            except IndexError:
                logger.warning(f'Exception on {el[0]} for user {el[1]}')
                continue

            final_price = catch.replace(' ', '').replace('&nbsp;','')[37:-7]
            wb_search_title = driver.find_element(By.CLASS_NAME, "product-page__header")
            couple = (wb_search_title.text.replace('\n', ' '), int(final_price))

            with transaction_sync() as cur:
                cur.execute(
                    f'''INSERT INTO tracker ( article, name, price, userid, data )
                        VALUES ( {el[0]}, '{couple[0]}', {couple[1]}, {el[1]}, {int(time.time())});'''
                    )
            logger.debug(f'Successfull commit for {el}, {couple}')
            
            time.sleep(random.randrange(8, 15))

    interval = random.randrange(3600, 4800)
    logger.debug(f'Sleep for {interval}')
    try:    
        time.sleep(interval)
    except KeyboardInterrupt:
        print('Goodbye!')