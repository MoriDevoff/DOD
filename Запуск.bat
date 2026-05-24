@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
title Где я? — запуск

cd /d "%~dp0"
echo.
echo ========================================
echo   Где я? — запуск из исходников
echo ========================================
echo.

if not exist "my_django_project\launcher.py" (
    echo [ОШИБКА] Не найден файл my_django_project\launcher.py
    echo.
    echo Запускайте этот bat из КОРНЯ распакованного архива,
    echo где видны папки: my_django_project, release
    echo.
    goto :fail
)

cd /d "%~dp0my_django_project"

set "PY_EXE="
for %%V in (3.14 3.13 3.12) do (
    py -%%V -c "import sys" >nul 2>&1
    if !errorlevel! equ 0 (
        set "PY_EXE=py -%%V"
        goto :found_py
    )
)

python -c "import sys; raise SystemExit(0 if sys.version_info[:2]>=(3,12) else 1)" >nul 2>&1
if !errorlevel! equ 0 set "PY_EXE=python"

:found_py
if not defined PY_EXE (
    echo [ОШИБКА] Python 3.12+ не найден.
    echo.
    echo 1. Установите с https://www.python.org/downloads/
    echo 2. При установке включите "Add python.exe to PATH"
    echo 3. Перезапустите этот файл
    echo.
    goto :fail
)

echo Используется: !PY_EXE!
echo Подождите, идёт запуск сервера...
echo Окно можно закрыть через Ctrl+C после открытия сайта.
echo.

!PY_EXE! launcher.py
set "ERR=!ERRORLEVEL!"
if !ERR! neq 0 goto :fail
exit /b 0

:fail
if not defined ERR set "ERR=1"
echo.
echo [ОШИБКА] Запуск не удался (код !ERR!).
if exist "launcher_error.log" (
    echo.
    echo --- launcher_error.log ---
    type "launcher_error.log"
    echo --- конец лога ---
)
echo.
pause
exit /b !ERR!
