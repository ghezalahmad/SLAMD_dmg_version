from setuptools import setup
import os
import shutil
import PIL.Image  # Ensure PIL is collected by py2app
import threading
import time

APP = ['run_slamd.py']

RESOURCE_DIRS = [
    'slamd/templates',
    'slamd/static',
    'slamd/libs',
    'slamd/common',
    'slamd/discovery/templates',
    'slamd/discovery/static',
    'slamd/formulations/templates',
    'slamd/formulations/static',
    'slamd/materials/templates',
    'slamd/materials/static',
    'slamd/design_assistant/templates',
    'slamd/design_assistant/static'
]

# ✅ Watchdog thread to remove the conflicting dist-info folder during py2app build
def watch_and_delete_conflict():
    conflict_path = os.path.join(
        'build', 'bdist.macosx-15.0-arm64', 'python3.11-standalone',
        'app', 'collect', 'backports.tarfile-1.2.0.dist-info'
    )
    while True:
        if os.path.exists(conflict_path):
            print(f"🧹 Removing conflicting directory: {conflict_path}")
            try:
                shutil.rmtree(conflict_path)
            except Exception as e:
                print(f"⚠️ Failed to remove: {e}")
        time.sleep(0.5)

# 🔧 Start background thread before build
threading.Thread(target=watch_and_delete_conflict, daemon=True).start()

OPTIONS = {
    'iconfile': 'slamd.icns',
    'packages': [
        'flask', 'jinja2', 'py4j', 'lolopy', 'werkzeug',
        'pandas', 'numpy', 'scipy', 'sklearn', 'plotly'
    ],
    'includes': [
        'encodings', 'idna.idnadata',
        'PIL.Image', 'pkg_resources', 'jaraco.text', 'backports.tarfile'
    ],
    'excludes': ['PyQt6', 'PyQt5', 'PyInstaller', 'imp'],
    'resources': RESOURCE_DIRS,
    'optimize': 1,
    'plist': {
        'CFBundleName': 'SLAMD',
        'CFBundleDisplayName': 'SLAMD',
        'CFBundleGetInfoString': "SLAMD for MacOS",
        'CFBundleIdentifier': 'com.slamd.app',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSPrincipalClass': 'NSApplication',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
