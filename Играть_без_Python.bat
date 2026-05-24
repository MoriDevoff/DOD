@echo off
chcp 65001 >nul
setlocal

set "EXE=%~dp0release\WhereIAm.exe"

if not exist "%EXE%" (
    echo.
    echo Файл WhereIAm.exe не найден: release\WhereIAm.exe
    echo.
    echo Разработчик должен собрать его один раз:
    echo   my_django_project\build_onefile.bat
    echo.
    echo Либо скачайте готовый exe из Releases на GitHub.
    echo.
    pause
    exit /b 1
)

start "" "%EXE%"
