# **Document_Processing_Service (AsDocProc)**

**Микросервисная система асинхронной обработки и каталогизации документов.**

---

## 🎯 **Цель проекта**

Проектирование и разработка программного обеспечения для автоматизации процессов загрузки, анализа и преобразования файлов различных форматов с использованием асинхронных очередей задач для обеспечения высокой доступности системы.

---

## 📂 **Структура проекта**

```arduino
    doc_processor/
├── docker/
│   ├── backend/
│   ├── nginx/
│   └── postgres/
│
├── src/
│   ├── config/                # settings, urls, celery
│   │   ├── settings/
│   │   ├── celery.py
│   │   └── urls.py
│   │
│   ├── apps/
│   │   └── documents/
│   │       ├── api/
│   │       │   ├── serializers.py
│   │       │   ├── views.py
│   │       │   └── urls.py
│   │       │
│   │       ├── services/
│   │       │   ├── validators.py
│   │       │   ├── processors.py
│   │       │   └── storage.py
│   │       │
│   │       ├── tasks/
│   │       │   ├── document_tasks.py
│   │       │   └── cleanup_tasks.py
│   │       │
│   │       ├── models.py
│   │       ├── admin.py
│   │       ├── apps.py
│   │       └── tests/
│   │
│   └── manage.py
│
├── docker-compose.yml
├── Dockerfile
├── README.md
└── .env

```