# Cash Flow Management System

> Веб-сервис для управления движением денежных средств (ДДС)  

---

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone git@github.com:Muta-Mad/cash_flow.git
cd cash_flow
```

### 2. Настройка виртуального окружения

#### Linux / macOS
```bash
python3 -m venv venv
venv/bin/activate
```

#### Windows
```bash
python -m venv venv
source venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

Создайте таблицы в базе данных SQLite на основе Django-моделей

### 4. Применение миграций

#### Linux / macOS
```bash
python3 manage.py migrate
```
#### Windows
```bash
python manage.py migrate
```

### 5. Создание суперпользователя (администратора)

Для доступа к интерфейсу управления записями и справочниками создайте аккаунт администратора:
#### Linux / macOS
```bash
python3 manage.py createsuperuser
```
#### Windows

```bash
python manage.py createsuperuser
```

Вам будет предложено ввести username, email и пароль.

### 6. Запуск веб-сервиса

Запустите локальный сервер разработки Django:
#### Linux / macOS
```bash
python3 manage.py runserver
```
#### Windows
```bash
python manage.py runserver
```
После этого проект будет доступен в вашем браузере по адресу:

**http://127.0.0.1:8000/admin/**