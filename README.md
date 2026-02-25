# Сервис обработки загружаемых документов (AcDocProc)

Микросервисная система асинхронной обработки и каталогизации документов.

---

## 🎯 Цель проекта

Проектирование и разработка программного обеспечения для автоматизации процессов загрузки, анализа и обработки загружаемых документов с использованием асинхронных очередей задач для обеспечения высокой доступности системы.

---

## 📂 Структура проекта
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

---

## 🧩 Общий сценарий

### 📤 Загрузка документов

- Авторизованный пользователь может загрузить один или несколько файлов

- Поддержка multipart/form-data

- Автоматическая группировка в batch_id

- Создание UUID уникального идетнификационного номера

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

    Событие  	        Кому	        Когда
    Загрузка документа	Администратору	После успешной загрузки
    Изменение статуса	Пользователю	После изменения в админке

### 📖 API Документация

    Swagger: /swagger/

    ReDoc: /redoc/

---

## 🏗 Архитектура

    Python 3.14
    Django - обработка HTTP запросов
    PostgreSQL - хранение данных
    Django REST Framework - API
    Celery - ассинхронные задачи
    Redis - брокер сообщений
    Docker - контейнеризация
    CI/CD - методология автоматизации
    drf-yasg (Swagger) - документация
    Pytest - тестирование

---

## ⚙️ Клонирование

    git clone git@github.com:cardinal3300/Document_Processing_Service.git

---

## 🐳 Запуск через Docker (рекомендуется)
    docker compose up -d --build

### ▶ Применить миграции

    docker compose exec backend python manage.py migrate

### ▶ Создать суперпользователя

    docker compose exec backend python manage.py createsuperuser

### 📍 Сервис будет доступен:

    API → http://localhost:80/api/

    Swagger → http://localhost:80/swagger/

    Admin → http://localhost:80/admin/

---

## 📊 Статусы документа

- Pending — На модерации

- Approved — Подтверждён

- Rejected — Отклонён

---

## 🏁 Happy Path

    Регистрация (Simple_JWT)
            │
            ▼
    Пользователь
            │
            ▼
    POST /api/upload/
            │
            ▼
    Создание UUID / batch_id
            │
            ▼
    Сохранение документов 'Pending' = "На модерации"
            │
            ▼
    Celery → Email админу
            │
            ▼
    Администратор (Django Admin)
            │
            ├── 'Approve' → статус = "Подтверждён"
            │
            ├── 'Reject' → статус = "Отклонён"
            │
            ▼
    Celery → Email пользователю

---

## 🧩 Покрытие тестами

Покрыто:

- Upload API (Happy Path)

- Email-уведомления

- Celery tasks

- Валидация

- Сервисы

---

## 👨‍💻 Автор

    Igor Zherdev
    
    Backend Developer