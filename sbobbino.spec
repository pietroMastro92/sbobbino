# sbobbino.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['sbobbino.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('whisper.cpp/', 'whisper.cpp'),
        ('whisper.cpp/models/', 'whisper.cpp/models'),
        ('build_whisper.sh', '.'),
        ('requirements.txt', '.'),
        ('config.json', '.'),

    ],
    hiddenimports=['encodings', 'codecs'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='sbobbino',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    onefile=True,
    windowed=True,
    console=False,  # Ensure windowed application
    icon='icon.png'  # Path to your icon file
)

app = BUNDLE(
    exe,
    name='sbobbino.app',
    icon='icon.png',
    bundle_identifier='com.pietromastro.sbobbino',
)


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='sbobbino',
)
