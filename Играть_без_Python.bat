@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions
title Где я? — запуск exe

cd /d "%~dp0"
echo.
echo ========================================
echo   Где я? — запуск без Python
echo ========================================
echo.

set "EXE=%~dp0release\WhereIAm.exe"

if not exist "%EXE%" (
    echo [ОШИБКА] Нет файла: release\WhereIAm.exe
    echo.
    echo Скачайте полный архив с GitHub ^(exe должен быть в release\^)
    echo или соберите: Собрать_exe.bat
    echo или запустите: Запуск.bat ^(нужен Python^)
    echo.
    goto :fail
)

echo Запуск %EXE%
echo Дождитесь открытия браузера: http://127.0.0.1:8000/
echo.

start /wait "" "%EXE%"

set "ERR=%ERRORLEVEL%"
if exist "%~dp0release\launcher_error.log" (
    echo.
    echo --- launcher_error.log ---
    type "%~dp0release\launcher_error.log"
    echo --- конец лога ---
)

if "%ERR%" neq "0" (
    echo.
    echo [ОШИБКА] Программа завершилась с кодом %ERR%
    goto :fail
)

echo.
echo Программа завершена.
pause
exit /b 0

:fail
pause
exit /b 1
