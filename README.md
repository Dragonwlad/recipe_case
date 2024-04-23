# Описание проекта

API сервис для создания рецептов, с автоматической выгрузкой рецептов с VK сообщества.

Описание:
* Регистрация через почту и пароль;
* Создавать/редактировать/удалять рецепты;
* 

## Технологии
* Backand: Django REST API, Redis, Celery, VK API, Unittest, Djoser

## Как запустить проект локально на Windows:

Клонировать репозиторий:

`git clone git@github.com:Dragonwlad/recipe_case.git`

Перейти в папку с проектом, создать и активировать виртуальное окружение, установить зависимости, сделать миграции:

`cd recipe_testcase/recipe_testcase`

Установить версию питона:

`sudo apt install python3.10-venv`

`python -m venv venv`

`source venv/Scripts/activate`

`pip install -r requirements.txt`

`python manage.py migrate`


### Запустить Redis

1. Установить и запустить Docker
2. В терминале вашего IDE выполнить загрузку образа и запустить контейнер с Redis:

`docker pull redis:latest`

`docker run --name redis-server -p 6379:6379 -d redis:latest`

### Запустить БД Postgres

1. Запустить БД
2. Внести данные БД в проект в .env по шаблону .env.example

### Запустить Backend

В папке проекта recipe_testcase, с активированым venv выполнить команду: 

`python manage.py runserver`


### Запустить Celery

С активированым venv, запущеным backend и контейнером Redis и выполнить в отдельном терминале:

`celery --app=recipe_testcase worker --loglevel=info --pool=solo`

Еще в одном терминале:

`celery -A recipe_testcase beat -l info`

### Доступные URL:

* http://127.0.0.1:8000/admin/
* http://127.0.0.1:8000/redoc/ 
* http://127.0.0.1:8000/api/recipes/
* http://127.0.0.1:8000/api/ingredients/

### Документация по проекту:

* http://127.0.0.1:8000/redoc/ 


## Автор:
[Владислав Кузнецов](https://github.com/Dragonwlad)
