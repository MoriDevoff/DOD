@echo off
chcp 65001 >nul
cd /d "%~dp0my_django_project"
call build_onefile.bat
if errorlevel 1 pause
exit /b %ERRORLEVEL%
