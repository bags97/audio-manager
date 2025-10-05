# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file per Audio Manager Teatrale
Genera eseguibili standalone per Windows, macOS e Linux
"""

import sys
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Determina il tipo di sistema operativo
is_windows = sys.platform.startswith('win')
is_macos = sys.platform == 'darwin'
is_linux = sys.platform.startswith('linux')

# Nome dell'eseguibile in base al sistema operativo
exe_name = 'AudioManager'
if is_windows:
    exe_name = 'AudioManager.exe'

# Verifica esistenza file icona (opzionale)
icon_file = None
if is_windows and Path('icon.ico').exists():
    icon_file = 'icon.ico'
elif is_macos and Path('icon.icns').exists():
    icon_file = 'icon.icns'

# Raccolta delle dipendenze e dati
hidden_imports = [
    'sounddevice',
    'soundfile',
    'numpy',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'tkinter',
    'threading',
    'json',
    'dataclasses',
]

# Raccogli tutti i moduli di matplotlib
hidden_imports += collect_submodules('matplotlib')

# Dati binari necessari per soundfile (libsndfile)
datas = []
datas += collect_data_files('soundfile', include_py_files=False)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Nessuna console per applicazione GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,  # Usa l'icona solo se esiste
)

# Per macOS, crea un bundle .app
if is_macos:
    app = BUNDLE(
        exe,
        name='AudioManager.app',
        icon=icon_file,  # Usa l'icona solo se esiste
        bundle_identifier='com.platea.audiomanager',
        info_plist={
            'CFBundleName': 'Audio Manager Teatrale',
            'CFBundleDisplayName': 'Audio Manager',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': 'True',
            'NSMicrophoneUsageDescription': 'Audio Manager needs access to audio devices for playback',
        },
    )
