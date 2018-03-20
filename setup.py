from setuptools import setup, find_packages

setup(
    name='colin',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
        'six',
        'conu'
    ],
    entry_points={
        'console_scripts': [
            'colin = colin.cli.colin:cli',
        ],
    },
)
