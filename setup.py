# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

APP_NAME = "ZGIRC时间同步"
VERSION = "4.1"
DESCRIPTION = "专业的时间同步工具，支持GUI界面、自动同步、开机自启动和一键更新"
AUTHOR = "ZGIRC Dev Team"
LICENSE = "MIT"
PYTHON_REQUIRES = ">=3.7"

setup(
    name="zgirc-time-sync",
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    license=LICENSE,
    python_requires=PYTHON_REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.28.0',
        'pywin32>=306',
    ],
    entry_points={
        'console_scripts': [
            'zgirc-time-sync=time:main',
        ],
    },
    data_files=[
        ('.', ['wget.exe']),
    ],
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'ascii': False,
            'packages': ['requests', 'ctypes'],
            'excludes': ['tkinter'],
        }
    },
    windows=[
        {
            'script': 'time.py',
            'icon_resources': [],
            'dest_base': 'ZGIRC_TimeSync',
        },
    ],
)
