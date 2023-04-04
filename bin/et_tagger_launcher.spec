# -*- mode: python ; coding: utf-8 -*-

import sys ; 

sys.setrecursionlimit(sys.getrecursionlimit() * 5000)

block_cipher = None


a = Analysis(
    ['et_tagger_launcher.py'],
    pathex=['', ],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='BFSU Stanza Tagger 1.1 [ET]',
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
    icon=['E:\\Pyinstaller\\BFSUStanViz\\bin\\resources\\ico\\logo.ico'],
)
