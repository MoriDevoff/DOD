@echo off
setlocal

cd /d "%~dp0"

echo Installing project dependencies...
py -3 -m pip install -r requirements.txt
py -3 -m pip install pyinstaller Pillow

echo Running Django system checks...
py -3 manage.py check
if errorlevel 1 goto :error

echo Building one-file executable...
py -3 -m PyInstaller ^
  --onefile ^
  --noconsole ^
  --name WhereIAm ^
  --add-data "static;static" ^
  --add-data "media;media" ^
  --add-data "db.sqlite3;." ^
  --add-data "mainpage\templates;templates" ^
  launcher.py
if errorlevel 1 goto :error

echo.
echo Build completed.
echo The executable is here: dist\WhereIAm.exe
goto :eof

:error
echo.
echo Build failed. Check the output above.
exit /b 1