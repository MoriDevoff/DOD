@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions
title Где я? — сборка exe

cd /d "%~dp0"
echo.
echo ========================================
echo   Сборка WhereIAm.exe
echo ========================================
echo.

if not exist "my_django_project\build_onefile.bat" (
    echo [ОШИБКА] Не найден my_django_project\build_onefile.bat
    echo Запускайте из корня распакованного архива.
    goto :fail
)

cd /d "%~dp0my_django_project"
call build_onefile.bat
set "ERR=%ERRORLEVEL%"
if %ERR% neq 0 goto :fail

echo.
echo Успех. Запускайте: Играть_без_Python.bat
pause
exit /b 0

:fail
echo.
echo [ОШИБКА] Сборка не удалась.
pause
exit /b 1
