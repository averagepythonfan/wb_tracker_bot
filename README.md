## Телеграм бот для трекинга цен на маркетплейсе Wildberries.

Учебный проект, основная цель которого показать моё умение проектировать микросервисную архитектуру на базе Docker,
также продемонстрировать навыки написания понятного читаемого кода на Python; декларативный подход к написанию приложения;
знание базовых запросов языка SQL.

Основной стек: Python 3.10, Docker, aiogram, SQLAlchemy, Selenium.

## Весь проект состоит из 4 контейнеров:
* Телеграм Бот на aiogram 2.25
* Реляционной базы данных Postgres
* Синхронного скрипта для парсинга с помощью Selenium
* Контейнер с браузером Firefox и вебдрайвером Geckodriver

## Принцип работы:
1. Пользователь автоматически регистрируется в базе данных (таблица users) с 3 трекерами
2. Добавляет артикулы товаров для отслеживания (таблица products)
3. Страница с товаром автоматически парсится каждые 1-1,5 часа. Цена заносится в таблицу trackers.
4. Если цена товара меняет своё значение, пользователю приходит уведомление.

## Для начала рабооты с ботом нужно (преполагается, что вы находитесь на сервере с debian-подобной операционной системой):
Сперва скачать репозитории с GitHub
> :$ git clone https://github.com/averagepythonfan/wb_tracker_bot.git

Затем сделать файл init.sh исполняемым и выполнить его
> :$ chmod +x init.sh
> :$ ./init.sh

Далее нужно переименовать файл с переменными окружения .env.example на .env
> :$ mv .env.example .env

Замените все пропущенные значения на ваши, можете воспользоваться стандартными редакторами nano или vi
> :$ nano .env

После замены можно запускать нашего бота со всей его прилагающейся архитектурой.
Чтобы запустить контейнеры в режиме detached, воспользуйтесь флагом -d в команде:
> :$ docker compose up -d
