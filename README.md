# Проект сбора пожертвований на нужды котиков написанный на FastAPI.

### Описание

QRkot - это API сервиса по сбору средств для финансирования благотворительных проектов. В сервисе реализована возможность регистрации пользователей, добавления благотворительных проектов и пожертвований, которые распределяются по открытым проектам.

## Stack

Python 3.8, FastAPI 0.78, aiogoogle 5.4.0

### Установка, Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

https://github.com/dardali/cat_charity_fund

```
git clone 
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создайте файл .env со следующим содержанием:

```
APP_TITLE=Ваши данные
DATABASE_URL=Ваши данные
SECRET=Ваши данные
FIRST_SUPERUSER_EMAIL=Ваши данные
FIRST_SUPERUSER_PASSWORD=Ваши данные
TYPE=Ваши данные
PROJECT_ID=Ваши данные
PRIVATE_KEY_ID=Ваши данные
PRIVATE_KEY=Ваши данные
CLIENT_EMAIL=Ваши данные
CLIENT_ID=Ваши данные
AUTH_URI=Ваши данные
TOKEN_URI=Ваши данные
AUTH_PROVIDER_X509_CERT_URL=Ваши данные
CLIENT_X509_CERT_URL=Ваши данные
UNIVERSE_DOMAIN=Ваши данные
EMAIL=Ваши данные
```

Запустить проект:

```
uvicorn app.main:app --reload
```

Документация по API проекта можно найти в файле openapi.json, запустить её можно на сайте redoc.
