@echo off
chcp 65001 >nul
setlocal EnableExtensions

cd /d "%~dp0my_django_project"
if errorlevel 1 (
    echo Не найдена папка my_django_project.
    pause
    exit /b 1
)

set "PY_CMD="
for %%V in (3.14 3.13 3.12) do (
    py -%%V -c "import sys" >nul 2>&1
    if not errorlevel 1 (
        set "PY_CMD=py -%%V"
        goto :run
    )
)

echo.
echo Python 3.12+ не найден.
echo Установите с https://www.python.org/downloads/
echo При установке отметьте "Add python.exe to PATH".
echo.
pause
exit /b 1

:run
echo Запуск «Где я?»...
echo.
%PY_CMD% launcher.py
set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" pause
exit /b %ERR%
