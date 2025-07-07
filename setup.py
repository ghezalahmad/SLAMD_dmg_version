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
    'iconfile': 'slamd.icns',  # optional, only if you want a custom app icon
    'includes': ['encodings', 'idna.idnadata'],
    'packages': ['flask', 'jinja2', 'py4j', 'lolopy', 'werkzeug', 'pandas', 'numpy', 'scipy', 'sklearn', 'plotly'],
    'excludes': ['PyQt6', 'PyQt5', 'PyInstaller'],
    'resources': RESOURCES,
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
