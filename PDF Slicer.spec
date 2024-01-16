# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=['./.venv/lib/python3.11/site-packages'],
    binaries=[],
    datas=[('./resources/pdf_color_2.png', './resources')],
    hiddenimports=['PySide6', 'PyPDF2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PDF Slicer',
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
    icon=['resources/slicer.ico'],
)
app = BUNDLE(
    exe,
    name='PDF Slicer.app',
    icon='./resources/slicer.ico',
    bundle_identifier=None,
)
