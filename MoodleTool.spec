# PyInstaller Spec-Datei für erweiterte Build-Konfiguration
# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# Plattform-spezifisches Icon
icon_file = None
if sys.platform == 'darwin':
    icon_file = 'icon.icns'
elif sys.platform == 'win32':
    icon_file = 'icon.ico'
# Linux verwendet kein Icon in der EXE

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database.py', '.'),
        ('dialogs.py', '.'),
        ('exporter.py', '.'),
        ('main_window.py', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='MoodleTool',
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
    icon=icon_file,
)

# macOS App Bundle (nur auf macOS)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='MoodleTool.app',
        icon='icon.icns',
        bundle_identifier='at.htlpinkafeld.moodle-tool',
        version='3.0.0',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
        },
    )
