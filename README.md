# Где я? (WhereIAm)

Веб-игра-викторина по угадыванию места на карте: режим **территории СФУ** и режим **Красноярска**.  
Пользователь смотрит фотографию, отмечает предполагаемое место на карте (Leaflet + OpenStreetMap) и получает очки в зависимости от расстояния до правильной точки. Есть таблица рекордов.

**Стек:** [Django](https://www.djangoproject.com/) 6.x, SQLite, шаблоны HTML + CSS + JavaScript.  
Карта подключается через **Leaflet** и тайлы OSM с CDN (отдельная установка не нужна). Шрифты — **Google Fonts** (по ссылке в шаблонах).

---

## Требования

| Компонент | Версия |
|-----------|--------|
| **Python** | **3.12+** (нужен для Django 6) |
| pip | актуальный |

Проверка версии Python:

```bash
python --version
```

---

## Что установить (библиотеки)

Из корня репозитория все зависимости Python перечислены в файле:

**`my_django_project/requirements.txt`**

Сейчас там только **Django** (остальное — стандартная библиотека Python и фронтенд по CDN).

Установка в виртуальное окружение (рекомендуется):

```bash
# Windows (PowerShell / cmd)
cd путь\к\WhereIAm
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r my_django_project/requirements.txt
```

```bash
# Linux / macOS
cd /path/to/WhereIAm
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r my_django_project/requirements.txt
```

**Отдельно скачивать Leaflet/npm не нужно** — он подключается из шаблонов (`unpkg.com`). Для работы нужен доступ в интернет при открытии страниц с картой и шрифтами.

---

## Как запустить локально

1. Активируй виртуальное окружение (см. выше).

2. Перейди в каталог проекта Django:

   ```bash
   cd my_django_project
   ```

3. Примени миграции (создастся `db.sqlite3`):

   ```bash
   python manage.py migrate
   ```

4. (Опционально) Создай суперпользователя для входа в админку:

   ```bash
   python manage.py createsuperuser
   ```

5. Запусти сервер разработки:

   ```bash
   python manage.py runserver
   ```

6. Открой в браузере: **http://127.0.0.1:8000/**

Админка Django: **http://127.0.0.1:8000/admin/** (если создавал `createsuperuser`).

---

## Структура репозитория (кратко)

```
WhereIAm/
├── README.md
├── .gitignore
└── my_django_project/
    ├── manage.py
    ├── requirements.txt
    ├── mysite/              # настройки проекта Django
    ├── mainpage/            # приложение: модели, вьюхи, шаблоны
    ├── static/mainpage/     # CSS, JS, фоновые картинки, логотип
    └── media/               # загружаемые фото локаций (если используются)
```

---

## Выгрузка на GitHub

1. Создай репозиторий на GitHub (без README, если уже есть локальный).

2. В папке `WhereIAm`:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: WhereIAm"
   git branch -M main
   git remote add origin https://github.com/ВАШ_ЛОГИН/ИМЯ_РЕПО.git
   git push -u origin main
   ```

3. **Не публикуй в открытом виде** `SECRET_KEY` из `mysite/settings.py`. Перед продакшеном вынеси его в переменные окружения и смени ключ. Для учебного репозитория можно оставить как есть, но для публичного деплоя — обязательно исправь.

---

## Полезные команды

| Команда | Назначение |
|---------|------------|
| `python manage.py runserver` | Запуск dev-сервера |
| `python manage.py migrate` | Применить миграции БД |
| `python manage.py makemigrations` | Создать миграции после изменения моделей |

---

Если что-то не запускается — проверь версию Python (**3.12+**), что активировано venv и что команды выполняются из каталога `my_django_project`.
