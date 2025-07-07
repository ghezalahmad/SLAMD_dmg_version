from setuptools import setup
import os
import glob

APP = ['run_slamd.py']

# SLAMD has templates and static files in multiple submodules, so we include them all.
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

# Flatten resource folder list (just folder paths, py2app will include content recursively)
RESOURCES = [os.path.join(*d.split('/')) for d in RESOURCE_DIRS]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'slamd.icns',
    'packages': ['flask', 'jinja2', 'py4j', 'lolopy', 'werkzeug', 'pandas', 'numpy', 'scipy', 'sklearn', 'plotly'],
    'excludes': ['PyQt6', 'PyQt5', 'PyInstaller'],
    'resources': RESOURCE_DIRS,
    'optimize': 1,
    'includes': ['encodings', 'idna.idnadata'],
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
