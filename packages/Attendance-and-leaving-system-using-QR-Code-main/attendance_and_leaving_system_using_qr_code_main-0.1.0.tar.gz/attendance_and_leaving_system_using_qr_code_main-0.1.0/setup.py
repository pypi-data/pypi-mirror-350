# setup.py
from setuptools import setup, find_packages

setup(
    name='Attendance-and-leaving-system-using-QR-Code-main',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.0', # or your version
    ],
    entry_points={
        'console_scripts': [],
    },
)