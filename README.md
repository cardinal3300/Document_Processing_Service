# **Document_Processing_Service (🦾🤖👍_AsDocProc)**

**Микросервисная система асинхронной обработки и каталогизации документов.**

---

## 🎯 **Цель проекта**

Проектирование и разработка программного обеспечения для автоматизации процессов загрузки, анализа и преобразования файлов различных форматов с использованием асинхронных очередей задач для обеспечения высокой доступности системы.

---

## 📂 **Структура проекта**

```arduino
    AcDocProc/
        ├── .github/
        │       └── workflows/               
        │              └── ci.yml
        ├── config/                    # settings, urls, celery
        │     ├── settings/
        │     ├── celery.py
        │     └── urls.py        
        ├── documents/                 # Главное приложение 
        │       ├── migrations/
        │       ├── admin.py
        │       ├── apps.py
        │       ├── models.py
        │       ├── serializers.py
        │       ├── tasks
        │       ├── tests
        │       ├── urls.py
        │       ├── validators.py
        │       └── views.py
        ├── nginx/
        │     ├── Dockerfile
        │     └── nginx.conf
        ├── .env.semple
        ├── .gitignore
        ├── README.md
        ├── manage.py
        ├── Dockerfile
        ├── .flake8
        ├── requirements.txt
        └── docker-compose.yml  
```

---

## 🧩 Общий сценарий
### 📤 Загрузка документов

- Авторизованный пользователь может загрузить один или несколько файлов

- Поддержка multipart/form-data

- Автоматическая группировка в batch_id

### 🔎 Валидация

- Проверка типа файла

- Проверка размера

- Проверка количества файлов

- (при необходимости) антивирусная проверка

### ⚙ Асинхронная обработка

Используется:

- Celery

- Redis

После загрузки:

- 📩 Администратору отправляется email о новых документах

После изменения статуса:

- 📩 Пользователь получает email с обновлением статуса

### 👨‍💼 Админ-панель

Администратор может:

- Просматривать документы

- Менять статус (Pending, Approved, Rejected)

- Видеть владельца документа

- Скачивать загруженные файлы

### 📬 Email-уведомления

Отправляются автоматически:

```ardeno
    Событие  	        Кому	        Когда
    Загрузка документа	Администратору	После успешной загрузки
    Изменение статуса	Пользователю	После изменения в админке
```

### 📖 API Документация

Swagger: /swagger/

ReDoc: /redoc/

---

### 🏗 Архитектура

    config/
    documents/
    users/

### ⚙️ Установка и запуск

    🔹 1. Клонирование
    git clone <repo_url>
    cd AcDocProc

### 🐳 Запуск через Docker (рекомендуется)

    ▶ Запуск
    docker compose up --build

### ▶ Применить миграции

    docker compose exec web python manage.py migrate

### ▶ Создать суперпользователя
docker compose exec web python manage.py createsuperuser

### 📍 Сервис будет доступен:

    API → http://localhost:8000/api/
    
    Swagger → http://localhost:8000/swagger/
    
    Admin → http://localhost:8000/admin/

---

## 📊 Статусы документа

- Pending — ожидает проверки

- Approved — одобрен

- Rejected — отклонён

---

## 🧠 Технологии

- Python 3.12

- Django

- Django REST Framework

- Celery

- Redis

- PostgreSQL

- Docker

- drf-yasg (Swagger)

- Pytest

---

## 🏁 Happy Path

1. Пользователь регистрируется

2. Загружает документы

3. Администратор получает email

4. Администратор меняет статус

5. Пользователь получает email

6. Документ хранится в системе

## 🧩 Покрытие тестами

Покрыто:

- Upload API (Happy Path)

- Email-уведомления

- Celery tasks

- Валидация

- Сервисы

## 👨‍💻 Автор

Igor Zherdev

Backend Developer

