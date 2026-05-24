# Где я? (WhereIAm)

Веб-игра: угадайте место на карте по фотографии (режимы **СФУ** и **Красноярск**).

---

## Для пользователя — без Python

Нужен только один файл **`WhereIAm.exe`**.

1. Скачайте **`WhereIAm.exe`** из [GitHub Releases](https://github.com/ВАШ_ЛОГИН/ИМЯ_РЕПО/releases)  
   *(или возьмите `release/WhereIAm.exe` после сборки у разработчика)*.
2. Дважды щёлкните по exe — откроется браузер: **http://127.0.0.1:8000/**

Из репозитория (если exe уже собран): **`Играть_без_Python.bat`**.

> **Интернет** нужен для карты (OpenStreetMap) и шрифтов.

Подробнее: [release/README.txt](release/README.txt).

---

## Для разработчика — запуск из исходников

1. Python **3.12+** с [python.org](https://www.python.org/downloads/).
2. Дважды щёлкните **`Запуск.bat`** (установит зависимости и откроет сайт).

Или вручную:

```powershell
cd my_django_project
py -3.14 launcher.py
```

---

## Сборка exe (один раз, на вашем ПК)

```powershell
# из корня репозитория
.\Собрать_exe.bat
```

Или: `my_django_project\build_onefile.bat`

Результат:

| Путь | Назначение |
|------|------------|
| `release/WhereIAm.exe` | **Отдавать пользователям** (Python не нужен) |
| `my_django_project/dist/WhereIAm.exe` | Копия после PyInstaller |

Выкладывайте **`WhereIAm.exe`** в **GitHub Releases** (в git exe не коммитится — см. `.gitignore`).

Подробности: [EXE_BUILD_GUIDE.md](my_django_project/EXE_BUILD_GUIDE.md).

---

## Требования

| Компонент | Версия |
|-----------|--------|
| Python | **3.12+** (для запуска через `Запуск.bat`) |
| Django | 6.x (ставится автоматически) |

---

## Структура репозитория

```
WhereIAm/
├── Играть_без_Python.bat      ← запуск собранного exe
├── Собрать_exe.bat            ← сборка exe (нужен Python)
├── Запуск.bat                 ← запуск из исходников
├── release/
│   ├── README.txt
│   └── WhereIAm.exe           ← после сборки (в git не хранится)
├── README.md
└── my_django_project/
    ├── launcher.py            ← логика автозапуска
    ├── manage.py
    ├── requirements.txt
    ├── mysite/
    ├── mainpage/
    ├── static/mainpage/
    └── media/                 ← фото локаций (должны быть в репозитории)
```

После клона убедитесь, что в репозитории есть папка **`my_django_project/media/`** с фотографиями — иначе игра запустится, но картинки не отобразятся.

---

## Полезные команды (разработка)

Выполнять из `my_django_project` с активированным venv (по желанию):

| Команда | Назначение |
|---------|------------|
| `py -3.14 manage.py runserver` | Сервер без автозапуска браузера |
| `py -3.14 manage.py migrate` | Миграции БД |
| `py -3.14 manage.py loaddata mainpage/fixtures/initial_locations.json` | Стартовые локации |

---

## Выгрузка на GitHub

```bash
git init
git add .
git commit -m "WhereIAm"
git remote add origin https://github.com/ВАШ_ЛОГИН/ИМЯ_РЕПО.git
git push -u origin main
```

Перед публикацией:

- в git должны быть **`my_django_project/media/`** (фото) и **`static/`**;
- **`db.sqlite3`**, **`dist/`**, **`build/`**, **`release/WhereIAm.exe`** в git не попадают (см. `.gitignore`);
- exe для пользователей — через **GitHub Releases**.

---

## Если что-то не работает

| Проблема | Решение |
|----------|---------|
| «Python не найден» | Установите Python 3.12+ и перезапустите `Запуск.bat` |
| Порт 8000 занят | Закройте другой `runserver` или перезагрузите ПК |
| Нет фото в игре | Добавьте `media/` в репозиторий или выполните `loaddata` |
| Ошибка при запуске | Смотрите `my_django_project/launcher_error.log` |
