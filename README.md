# Описание проекта

API сервис для создания рецептов, с автоматической выгрузкой рецептов с VK сообщества.

Особенности:
* cоздавать рецепты;
* Добавление в избранное;
* Добавление в корзину;
* Скачивание списка ингредиентов к рецептам из корзины;
* Подписки на авторов.

## Технологии
* Backand: Django REST API, Redis, Celery

## Как запустить проект локально на Windows:

Клонировать репозиторий:

`git clone `

Перейти в папку с проектом, создать и активировать виртуальное окружение, установить зависимости, сделать миграции:

`cd recipe_testcase/recipe_testcase`

`python -m venv venv`

`source venv/Scripts/activate`

`pip install -r requirements.txt`

`python manage.py migrate`


### Запустить Redis

1. Установить и запустить Docker
2. В терминале вашего IDE выполнить загрузку образа и запустить контейнер с Redis:

`docker pull redis:latest`

`docker run --name redis-server -p 6379:6379 -d redis:latest`

### Запустить Backend

В папке проекта recipe_testcase, с активированым venv выполнить команду: 

`python manage.py runserver`



### Запустить Celery

С активированым venv, запущеным backend и контейнером Redis и выполнить в отдельном терминале:

`celery --app=recipe_testcase worker --loglevel=info --pool=solo`

Еще в одном терминале:

`celery -A recipe_testcase beat -l info`

