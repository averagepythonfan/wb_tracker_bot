import time
import random
import re
import requests
from logger import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from sqdb import transaction_sync
from config import TOKEN, COMMAND_EXECUTOR
from sqlalchemy import text


# set options for webdriver
options = Options()
options.add_argument("-headless")
options.set_capability("marionette", False)


# infinite update
while True:
    with webdriver.Remote(
            command_executor=f'http://{COMMAND_EXECUTOR}:4444',
            options=options) as driver:
        with transaction_sync() as cur:
            products = cur.execute(text('SELECT * FROM products;')).fetchall()
        logger.debug(f'Fetched pairs. Lenght : {len(products)}')
        for el in products:
            logger.debug(f'Start parsing for {el}')
            driver.get(f'https://www.wildberries.ru/catalog/{el[0]}/detail.aspx')

            time.sleep(2)

            try:
                catch = re.findall(
                    r'<ins class="price-block__final-price">.*?</ins>',
                    driver.page_source)[0]
            except IndexError as error:
                logger.warning(f'Exception on {el[0]} for user {el[1]}: {error}')
                continue

            final_price = catch.replace(' ', '').replace('&nbsp;', '')[37:-7]
            wb_search_title = driver.find_element(By.CLASS_NAME, "product-page__header")
            couple = (wb_search_title.text.replace('\n', ' '), int(final_price))

            with transaction_sync() as cur:
                cur.execute(text(f'''
                    INSERT INTO tracker ( article, name, price, userid, data )
                    VALUES ( {el[0]},
                            '{couple[0]}',
                            {couple[1]},
                            {el[1]},
                            {int(time.time())});'''))
            logger.debug(f'Successfull commit for {el}, {couple}')

            # FIX WHEN 0 TRACKERS
            with transaction_sync() as cur:
                products = cur.execute(text('SELECT * FROM products;')).fetchall()
            for el in products:
                with transaction_sync() as cur:
                    res = cur.execute(text(f'''
                        SELECT price, userid, name FROM tracker
                        WHERE article = {el[0]}
                        ORDER BY data DESC
                        LIMIT 2;
                    ''')).fetchall()
                if len(res) == 2:
                    if res[0][0] != res[1][0]:
                        requests.get(
                            f'https://api.telegram.org/bot{TOKEN}'
                            f'/sendMessage?chat_id={res[0][1]}&text='
                            f'?????? ?????????? {res[0][2]} ?????????????? ?????????????????? ?? {res[1][0]} ???? {res[0][0]}')
            time.sleep(random.randrange(8, 15))

    interval = random.randrange(3000, 3600)
    logger.debug(f'Sleep for {interval}')
    try:
        time.sleep(interval)
    except KeyboardInterrupt:
        print('Goodbye!')
