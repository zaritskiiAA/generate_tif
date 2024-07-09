#### Описание

Мок реализация для [Mycego](https://hh.ru/employer/9553033?hhtmFrom=vacancy)

# Cодержание

1. [Установка](#install)

2. [Запуск](#start)

3. [Информация](#info)


# 1.1 Подготовка <a id="install"></a>

Примечание: для работы над проектом желательно Python не ниже версии 3.11.

1. Клонировать на локальную машину

```
git clone <ssh или https>
```

2. Установка/запуск виртуального окружения.

```
python -m venv venv
```

```
source venv/Scripts/activate/
```

3. Инсталлим зависимости

```
pip install -r requirements.txt
```

# 2.1 Выполнение миграций и локальный запуск <a id="start"></a>

Примечание: команды выполняются из директории с модулем manage.py

```
python manage.py migrate
```

```
python manage.py runserver
```


# 3.1 Документация API <a id="info"></a>

После запуска localhost можно перейти на эндпоинт http://127.0.0.1:8000/swagger-ui/ и ознакомиться с работой API
