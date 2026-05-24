import os
import io
import socket
import sys
import threading
import time
import shutil
import webbrowser
from pathlib import Path


HOST = '127.0.0.1'
PORT = 8000
URL = f'http://{HOST}:{PORT}'


def project_root() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


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


def wait_for_server(host: str, port: int, timeout: float = 30.0) -> bool:
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


def show_error(message: str) -> None:
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, 'WhereIAm', 0x10)
    except Exception:
        pass


def write_error_log(root: Path, error: Exception) -> None:
    log_path = root / 'launcher_error.log'
    with log_path.open('a', encoding='utf-8') as log_file:
        log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {error!r}\n')


def run_django_server() -> None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

    root = project_root()
    os.chdir(root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    try:
        import django
        django.setup()

        from django.core.management import call_command

        command_output = io.StringIO()

        call_command('migrate', interactive=False, verbosity=0, stdout=command_output, stderr=command_output)

        call_command(
            'runserver',
            f'{HOST}:{PORT}',
            use_reloader=False,
            verbosity=0,
            stdout=command_output,
            stderr=command_output,
        )
    except Exception as error:
        write_error_log(root, error)
        show_error(f'Не удалось запустить проект.\n\nПодробнее: {error}')
        raise


def main() -> None:
    root = project_root()
    ensure_runtime_paths(root)
    seed_database(root)
    seed_media(root)

    server_thread = threading.Thread(target=run_django_server, daemon=False)
    server_thread.start()

    if not wait_for_server(HOST, PORT):
        show_error(f'Сервер не запустился на {URL}.')
        return

    open_browser()
    server_thread.join()


if __name__ == '__main__':
    main()