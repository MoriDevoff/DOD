# Где я? (WhereIAm)

Веб-игра: угадайте место на карте по фотографии (режимы **СФУ** и **Красноярск**).

---

## Скачали ZIP с GitHub?

1. Распакуйте архив.
2. Перейдите в папку release
3. Запустите файл WhereIAm.exe

> После обновления кода пересоберите: `Собрать_exe.bat` и закоммитьте новый exe.

---

**`release/WhereIAm.exe`** → браузер откроется на **http://127.0.0.1:8000/**

> **Интернет** нужен для карты и шрифтов.

---

## Разработчик — из исходников

```powershell
cd my_django_project
py -3.14 launcher.py
```

---

## Сборка exe

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
├── Собрать_exe.bat            ← сборка exe
├── Запуск.bat                 
├── release/
│   ├── README.txt
│   └── WhereIAm.exe           
├── README.md
└── my_django_project/
    ├── launcher.py            
    ├── manage.py
    ├── requirements.txt
    ├── mysite/
    ├── mainpage/
    ├── static/mainpage/
    └── media/                 ← фото локаций
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
- **`db.sqlite3`**, **`dist/`**, **`build/`** в git не попадают;
- **`release/WhereIAm.exe`** — в git **должен быть** (чтобы ZIP с GitHub работал сразу).

---

## Если что-то не работает

| Проблема | Решение |
|----------|---------|
| «Python не найден» | Установите Python 3.12+ и перезапустите `Запуск.bat` |
| Порт 8000 занят | Закройте другой `runserver` или перезагрузите ПК |
| Нет фото в игре | Добавьте `media/` в репозиторий или выполните `loaddata` |
| Ошибка при запуске | Смотрите `my_django_project/launcher_error.log` |
