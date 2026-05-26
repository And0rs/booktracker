# BookTracker

Веб-приложение для отслеживания прочитанных книг и написания рецензий.

## Быстрый старт

### Требования

- Python 3.10+
- Docker

### 1. Запустить PostgreSQL

```bash
docker run --name booktracker-db \
  -e POSTGRES_PASSWORD=booktracker \
  -e POSTGRES_DB=booktracker \
  -p 5432:5432 -d postgres
```

### 2. Клонировать и настроить

```bash
git clone <url>
cd booktracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Инициализировать БД

```bash
docker exec -i booktracker-db psql -U postgres -d booktracker < sql/create_db.sql
```

### 4. Запустить

```bash
python app.py
```

Открыть `http://127.0.0.1:5000`

### Тестовые пользователи

| Логин | Пароль | Роль |
|-------|--------|------|
| bob | 1234567 | Администратор |
| example | 123456 | Обычный пользователь |

## Стек

- **Frontend:** HTML5, Bootstrap 5, JavaScript
- **Backend:** Python, Flask, SQLAlchemy, Flask-Login
- **Database:** PostgreSQL

## Описание

5 страниц: каталог книг с поиском, страница книги (рецензии, статус чтения),
добавление книги, профиль со статистикой, вход/регистрация с переключением форм.

Валидация форм на чистом JavaScript без внешних библиотек.
