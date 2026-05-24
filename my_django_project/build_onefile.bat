@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "PY="
for %%V in (3.14 3.13 3.12) do (
    py -%%V -c "import sys" >nul 2>&1
    if !errorlevel! equ 0 (
        set "PY=py -%%V"
        goto :have_py
    )
)
python -c "import sys; raise SystemExit(0 if sys.version_info[:2]>=(3,12) else 1)" >nul 2>&1
if !errorlevel! equ 0 set "PY=python"

:have_py
if not defined PY (
    echo [ОШИБКА] Python 3.12+ не найден. https://www.python.org/downloads/
    exit /b 1
)

echo Используется: !PY!

if not exist "media\" (
    echo [ОШИБКА] Нет папки media\ с фотографиями.
    exit /b 1
)

echo [1/5] Зависимости...
!PY! -m pip install -r requirements.txt
if errorlevel 1 goto :error
!PY! -m pip install pyinstaller
if errorlevel 1 goto :error

echo [2/5] Подготовка базы...
if exist db.sqlite3 del /f db.sqlite3
!PY! manage.py migrate --noinput
if errorlevel 1 goto :error
!PY! manage.py loaddata mainpage/fixtures/initial_locations.json
if errorlevel 1 goto :error

echo [3/5] Проверка Django...
!PY! manage.py check
if errorlevel 1 goto :error

echo [4/5] Сборка exe (несколько минут)...
!PY! -m PyInstaller --noconfirm WhereIAm.spec
if errorlevel 1 goto :error

if not exist "dist\WhereIAm.exe" (
    echo [ОШИБКА] dist\WhereIAm.exe не создан.
    goto :error
)

echo [5/5] Копирование в release\...
if not exist "..\release" mkdir "..\release"
copy /Y "dist\WhereIAm.exe" "..\release\WhereIAm.exe" >nul

echo.
echo Готово: ..\release\WhereIAm.exe
exit /b 0

:error
echo.
echo [ОШИБКА] Сборка прервана.
exit /b 1
