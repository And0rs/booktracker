# BookTracker

Веб-приложение для отслеживания прочитанных книг и написания рецензий.

## Быстрый старт

### Требования

- Python 3.10+
- PostgreSQL (через Docker, Homebrew или apt)

### 1. Запустить PostgreSQL

#### Вариант A — через Docker

```bash
docker run --name booktracker-db \
  -e POSTGRES_PASSWORD=booktracker \
  -e POSTGRES_DB=booktracker \
  -p 5432:5432 -d postgres
```

#### Вариант B — установить PostgreSQL напрямую

**Ubuntu/Debian:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres psql -c "CREATE USER postgres PASSWORD 'booktracker';"
sudo -u postgres psql -c "CREATE DATABASE booktracker OWNER postgres;"
```

**macOS (Homebrew):**
```bash
brew install postgresql@16
brew services start postgresql@16
createdb booktracker    # суперпользователь = текущий пользователь
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

Отредактируй `.env` — в нём должен быть правильный `DATABASE_URL`:

- **Docker / Ubuntu:**
  ```
  DATABASE_URL=postgresql+psycopg://postgres:booktracker@localhost:5432/booktracker
  ```
- **macOS:**
  ```
  DATABASE_URL=postgresql+psycopg://localhost:5432/booktracker
  ```

### 3. Инициализировать БД

**Через Docker:**
```bash
docker exec -i booktracker-db psql -U postgres -d booktracker < sql/create_db.sql
```

**Напрямую (Ubuntu):**
```bash
psql -U postgres -d booktracker < sql/create_db.sql
```

**Напрямую (macOS):**
```bash
psql -d booktracker < sql/create_db.sql
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
