# QRkot_spreadseets

## Описание проекта:
### Проекты
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
### Пожертвования
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.
### Пользователи
Целевые проекты создаются администраторами сайта. Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых. Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

У адмимистратора имеется возможность получать отчеты о завершенных проектах в Google Sheets.

## Используемые технологии
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [FastAPI-Users](https://www.fastapi-users.github.io)
- [aioSQLite](aiosqlite.omnilib.dev)
- [Pydantic](pydantic.dev)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Google Sheets API](https://developers.google.com/sheets/api/guides/concepts?hl=en)
- [Google Drive API](https://developers.google.com/drive/api/guides/about-sdk?hl=en)



## Запуск проекта

1. Клонировать репозиторий:
```bash
git clone https://github.com/magicbuka/QRkot_spreadsheets.git
```

2. Создать виртуальное окружение:
```bash
python -m venv venv
```

3. Активировать виртуальное окружение и установить зависимости из ```requirements.txt```:
```bash
source venv/Scripts/activate
```
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

4. Применить миграции:
```bash
alembic upgrade head
```

5. Запустить проект:
```bash
uvicorn app.main:app --reload
```

При необходимости в корневой папке создайте файл *.env* и заполните своими данными:

```bash
APP_TITLE=         
APP_DESCRIPTION=   
DATABASE_URL=      
SECRET=
FIRST_SUPERUSER_EMAIL=
FIRST_SUPERUSER_PASSWORD=
EMAIL=
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```


## Документация проекта QRKot

[Swagger](http://127.0.0.1:8000/docs)
[ReDoc](http://127.0.0.1:8000/redoc)



Разработчик проекта [Baranova Anna](https://github.com/magicbuka)