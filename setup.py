from setuptools import setup, find_packages
from glob import glob
# python setup.py bdist_wheel in RoboArena folder


setup(
    name='RoboArena',
    version='1.0.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[
        ('code', glob('maps/*.json')),
        ('code', glob('res/*'))
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "numpy",
        "igraph",
        "pyqt5",
        "time",
        "json",
        "warnings",
        "sys",
        "os",
        "pathlib",
        "random",
        "copy"
    ]
)
