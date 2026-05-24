@echo off
chcp 65001 >nul
setlocal EnableExtensions

cd /d "%~dp0"

set "PY=py -3.14"
%PY% -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo Python 3.14 не найден. Установите с https://www.python.org/downloads/
    exit /b 1
)

if not exist "media\" (
    echo ОШИБКА: нет папки media\ с фотографиями. Игра не соберётся без медиа.
    exit /b 1
)

echo [1/5] Зависимости...
%PY% -m pip install -r requirements.txt -q
%PY% -m pip install pyinstaller -q

echo [2/5] Подготовка базы для упаковки...
if exist db.sqlite3 del /f db.sqlite3
%PY% manage.py migrate --noinput
if errorlevel 1 goto :error
%PY% manage.py loaddata mainpage/fixtures/initial_locations.json
if errorlevel 1 goto :error

echo [3/5] Проверка Django...
%PY% manage.py check
if errorlevel 1 goto :error

echo [4/5] Сборка WhereIAm.exe (может занять несколько минут)...
%PY% -m PyInstaller --noconfirm WhereIAm.spec
if errorlevel 1 goto :error

if not exist "dist\WhereIAm.exe" (
    echo Сборка завершилась, но dist\WhereIAm.exe не найден.
    goto :error
)

echo [5/5] Копирование в release\...
if not exist "..\release" mkdir "..\release"
copy /Y "dist\WhereIAm.exe" "..\release\WhereIAm.exe" >nul

echo.
echo Готово.
echo   Для разработчика:  dist\WhereIAm.exe
echo   Для пользователей: release\WhereIAm.exe
echo.
echo Передайте получателю файл release\WhereIAm.exe
echo (Python ему не нужен). Запуск — двойной щелчок.
goto :eof

:error
echo.
echo Сборка не удалась. Смотрите сообщения выше.
exit /b 1
