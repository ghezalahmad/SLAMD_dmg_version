from setuptools import setup
import glob

APP = ['run_slamd.py']

# Collect template files
template_files = glob.glob('slamd/templates/*.html')
static_files = glob.glob('slamd/static/*')
lib_files = glob.glob('slamd/libs/*')

DATA_FILES = [
    ('slamd/templates', template_files),
    ('slamd/static', static_files),
    ('slamd/libs', lib_files)
]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'slamd.icns',
    'packages': [
        'flask', 'jinja2', 'py4j', 'lolopy',
        'werkzeug', 'pandas', 'numpy', 'scipy',
        'sklearn', 'plotly', 'wtforms'
    ],
    'excludes': [
        'PyQt5', 'PyQt5.QtWebEngine', 'PyQt6',
        'PyQt6.QtWebEngine', 'PySide2', 'PySide6',
        'tkinter', 'wx', 'PyInstaller.hooks.hook-PyQt5.QtWebEngine'
    ]
}


setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
