# -*- mode: python ; coding: utf-8 -*-
# Сборка: py -3.14 -m PyInstaller WhereIAm.spec  (или build_onefile.bat)

from pathlib import Path

block_cipher = None
root = Path(SPECPATH)

datas = [
    (str(root / 'static'), 'static'),
    (str(root / 'media'), 'media'),
    (str(root / 'db.sqlite3'), '.'),
    (str(root / 'mainpage' / 'templates'), 'templates'),
    (str(root / 'mainpage' / 'migrations'), 'mainpage/migrations'),
    (str(root / 'mainpage' / 'fixtures'), 'mainpage/fixtures'),
]

hiddenimports = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.template.loaders.filesystem',
    'django.template.loaders.app_directories',
    'mainpage',
    'mysite',
]

a = Analysis(
    ['launcher.py'],
    pathex=[str(root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WhereIAm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
