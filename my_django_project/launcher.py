#!/usr/bin/env python3.14
"""
Единая точка запуска проекта «Где я?».
Двойной клик по Запуск.bat (в корне репозитория) или: py launcher.py
"""
from __future__ import annotations

import io
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8000
URL = f'http://{HOST}:{PORT}'
FIXTURE_PATH = 'mainpage/fixtures/initial_locations.json'


def ensure_stdio() -> None:
    """PyInstaller с --noconsole: stdout/stderr = None, Django падает на .write()."""
    for name in ('stdout', 'stderr'):
        stream = getattr(sys, name, None)
        if stream is None or not callable(getattr(stream, 'write', None)):
            setattr(
                sys,
                name,
                open(os.devnull, 'w', encoding='utf-8', errors='replace'),
            )


def safe_print(*args, **kwargs) -> None:
    ensure_stdio()
    try:
        print(*args, **kwargs)
    except (AttributeError, OSError):
        pass


def project_root() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def show_error(message: str) -> None:
    safe_print(message, file=sys.stderr)
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, 'Где я? — ошибка запуска', 0x10)
        except Exception:
            pass


def write_error_log(root: Path, error: BaseException) -> None:
    log_path = root / 'launcher_error.log'
    with log_path.open('a', encoding='utf-8') as log_file:
        log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {error!r}\n')


def ensure_runtime_paths(root: Path) -> None:
    for folder_name in ('media', 'staticfiles'):
        (root / folder_name).mkdir(parents=True, exist_ok=True)


def copy_tree_if_missing(source: Path, destination: Path) -> None:
    if not source.exists():
        return

    destination.mkdir(parents=True, exist_ok=True)
    for item in source.rglob('*'):
        relative_path = item.relative_to(source)
        target = destination / relative_path
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def seed_database(root: Path) -> None:
    database_path = root / 'db.sqlite3'
    if database_path.exists():
        return

    bundled_database = Path(getattr(sys, '_MEIPASS', root)) / 'db.sqlite3'
    if bundled_database.exists():
        shutil.copy2(bundled_database, database_path)


def seed_media(root: Path) -> None:
    media_root = root / 'media'
    bundled_media = Path(getattr(sys, '_MEIPASS', root)) / 'media'

    has_any_media = media_root.exists() and any(media_root.iterdir())
    if not has_any_media:
        copy_tree_if_missing(bundled_media, media_root)


def ensure_dependencies(root: Path) -> None:
    if getattr(sys, 'frozen', False):
        return

    try:
        import django  # noqa: F401
        return
    except ImportError:
        pass

    requirements = root / 'requirements.txt'
    if not requirements.exists():
        raise RuntimeError(f'Не найден файл зависимостей: {requirements}')

    safe_print('Устанавливаю зависимости (Django, Pillow)...')
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', '-r', str(requirements)],
        cwd=root,
    )


def wait_for_server(host: str, port: int, timeout: float = 60.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.25)
    return False


def open_browser() -> None:
    try:
        webbrowser.open_new(URL)
    except Exception:
        pass


def setup_django(root: Path) -> None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    os.chdir(root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    import django
    django.setup()


def ensure_database_ready() -> None:
    from django.core.management import call_command
    from mainpage.models import KrasLocation, SfuLocation

    frozen = getattr(sys, 'frozen', False)
    verbosity = 0 if frozen else 1
    output = io.StringIO()
    call_command(
        'migrate',
        interactive=False,
        verbosity=verbosity,
        stdout=output,
        stderr=output,
    )
    printed = output.getvalue().strip()
    if printed and not frozen:
        safe_print(printed)

    if SfuLocation.objects.exists() or KrasLocation.objects.exists():
        return

    fixture = project_root() / FIXTURE_PATH
    if not fixture.exists():
        safe_print('Внимание: база пуста, fixture не найден — добавьте локации вручную.')
        return

    safe_print('Загружаю стартовые локации...')
    call_command(
        'loaddata',
        FIXTURE_PATH,
        verbosity=verbosity,
        stdout=output,
        stderr=output,
    )


def run_django_server(server_error: list[BaseException]) -> None:
    root = project_root()
    try:
        setup_django(root)
        from django.core.management import call_command

        ensure_database_ready()

        frozen = getattr(sys, 'frozen', False)
        if not frozen:
            safe_print(f'\nСайт: {URL}\nОстановка: Ctrl+C в этом окне.\n')

        server_output = io.StringIO()
        call_command(
            'runserver',
            f'{HOST}:{PORT}',
            use_reloader=False,
            verbosity=0 if frozen else 1,
            stdout=server_output,
            stderr=server_output,
        )
    except Exception as error:
        write_error_log(root, error)
        server_error.append(error)
        show_error(f'Не удалось запустить проект.\n\n{error}')


def main() -> int:
    ensure_stdio()
    root = project_root()
    ensure_runtime_paths(root)

    if not getattr(sys, 'frozen', False):
        ensure_dependencies(root)

    seed_database(root)
    seed_media(root)

    server_error: list[BaseException] = []
    server_thread = threading.Thread(
        target=run_django_server,
        args=(server_error,),
        daemon=False,
    )
    server_thread.start()

    deadline = time.time() + 90.0
    while time.time() < deadline:
        if server_error:
            if not getattr(sys, 'frozen', False):
                safe_print(f'\nОшибка: {server_error[0]}\nСм. launcher_error.log\n')
            return 1
        if not server_thread.is_alive():
            show_error(
                'Сервер остановился при запуске.\n'
                f'См. launcher_error.log в папке:\n{root}'
            )
            return 1
        if wait_for_server(HOST, PORT, timeout=0.5):
            open_browser()
            server_thread.join()
            return 0
        time.sleep(0.25)

    show_error(
        f'Сервер не ответил на {URL} за 90 с.\n'
        f'Проверьте launcher_error.log в папке:\n{root}'
    )
    return 1


if __name__ == '__main__':
    ensure_stdio()
    exit_code = 0
    try:
        exit_code = main()
    except KeyboardInterrupt:
        safe_print('\nСервер остановлен.')
    except Exception as error:
        write_error_log(project_root(), error)
        show_error(f'Не удалось запустить проект.\n\n{error}')
        exit_code = 1

    if exit_code != 0 and not getattr(sys, 'frozen', False):
        safe_print('\nНажмите Enter, чтобы закрыть окно...')
        try:
            input()
        except EOFError:
            pass

    sys.exit(exit_code)
