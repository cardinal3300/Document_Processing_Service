# **Document_Processing_Service (AsDocProc)**

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
        │       ├── services
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