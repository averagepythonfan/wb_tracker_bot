from datetime import datetime
import time
import random
import re
import requests
import logging
from db import User, Product, Tracker
from db import session as Session
from config import TOKEN, COMMAND_EXECUTOR
from sqlalchemy import select, insert
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# set options for webdriver
options = Options()
options.add_argument("-headless")
options.set_capability("marionette", False)

# set logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    while True:
        with webdriver.Remote(
                command_executor=f'http://{COMMAND_EXECUTOR}:4444',
                options=options) as driver:
            with Session() as session:
                query = select(Product)
                result = session.execute(query)
                products = []
                for el in result.scalars():
                    products.append([el.article, el.user_id])
                logger.info(f'Fetched pairs. Lenght : {len(products)}')
            for el in products:
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

                with Session() as session:
                    values = {
                        'article': el[0],
                        'name': couple[0],
                        'price': couple[1],
                        'user_id': el[1],
                        'data': datetime.now()
                    }
                    query = insert(Tracker).values(**values)
                    session.execute(query)
                    session.commit()
                    logger.debug(f'Successfull commit for {el}, {couple}')

                with Session() as session:
                    query = select(Tracker).where(Tracker.article == el[0])\
                        .order_by(Tracker.data.desc())\
                        .limit(2)
                    res = session.execute(query)
                    prices = []
                    for price in res.scalars():
                        prices.append(price.price)
                    if prices[0] != prices[1]:
                        requests.get(
                                f'https://api.telegram.org/bot{TOKEN}'
                                f'/sendMessage?chat_id={el[1]}&text='
                                f'Ваш товар {el[0]} изменил стоимость с {prices[0]} на {prices[1]}')
                        logger.info(f'article {el[0]} change his prices from {prices[0]} to {prices[1]}')
                time.sleep(random.randrange(8, 15))
        interval = random.randrange(3000, 3600)
        logger.info(f'Sleep for {interval}')
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print('Goodbye!')

if __name__ == '__main__':
    main()
