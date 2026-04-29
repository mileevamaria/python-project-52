# Менеджер задач (Django)
[![Actions Status](https://github.com/mileevamaria/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/mileevamaria/python-project-52/actions)
[![python-package](https://github.com/mileevamaria/python-project-52/actions/workflows/python-package.yml/badge.svg)](https://github.com/mileevamaria/python-project-52/actions/workflows/python-package.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mileevamaria_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mileevamaria_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mileevamaria_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mileevamaria_python-project-52)

https://python-project-52-9faj.onrender.com

Веб-приложение для управления задачами с возможностью назначения исполнителей, отслеживания статусов и работы с метками. Проект реализован на Django и демонстрирует классический CRUD-подход с авторизацией пользователей.

### Возможности
- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление задач
- Назначение исполнителя задачи
- Добавление меток (labels) к задачам
- Отслеживание статусов (новая, в работе, завершена и т.д.)
- Фильтрация задач по статусу, исполнителю и меткам
- Интерфейс с использованием Bootstrap

### Стек технологий
* Python 3
* Django
* PostgreSQL (или SQLite для разработки)
* Bootstrap 5
* Gunicorn (для деплоя)

### Установка
```shell
git clone git@github.com:mileevamaria/python-project-52.git
brew install uv
make install
make render-start
```


