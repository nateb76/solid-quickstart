# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for vAI Send Mail.
Run: pyinstaller vai_send_mail.spec
"""

import os
import importlib

block_cipher = None

# Collect Streamlit data files (templates, static assets, etc.)
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

streamlit_data = collect_data_files("streamlit")
streamlit_hidden = collect_submodules("streamlit")

# App source files and templates
app_dir = os.path.dirname(os.path.abspath(SPEC))

app_data = [
    (os.path.join(app_dir, "app.py"), "vai_app"),
    (os.path.join(app_dir, "engine.py"), "vai_app"),
    (os.path.join(app_dir, "validation.py"), "vai_app"),
    (os.path.join(app_dir, "ai_checks.py"), "vai_app"),
    (os.path.join(app_dir, "postgrid_client.py"), "vai_app"),
    (os.path.join(app_dir, "templates_loader.py"), "vai_app"),
    (os.path.join(app_dir, "theme.py"), "vai_app"),
    (os.path.join(app_dir, "templates"), "vai_app/templates"),
    (os.path.join(app_dir, ".streamlit"), "vai_app/.streamlit"),
]

a = Analysis(
    ["launcher.py"],
    pathex=[app_dir],
    binaries=[],
    datas=streamlit_data + app_data,
    hiddenimports=streamlit_hidden + [
        "streamlit.web.cli",
        "streamlit.runtime.scriptrunner",
        "pandas",
        "openpyxl",
        "jinja2",
        "dotenv",
        "anthropic",
        "requests",
        "webview",
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
    [],
    exclude_binaries=True,
    name="vAI Send Mail",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    target_arch=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="vAI Send Mail",
)

app = BUNDLE(
    coll,
    name="vAI Send Mail.app",
    icon=None,
    bundle_identifier="com.vai.sendmail",
    info_plist={
        "CFBundleName": "vAI Send Mail",
        "CFBundleDisplayName": "vAI Send Mail",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
        "LSBackgroundOnly": False,
    },
)
