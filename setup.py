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
    data_files=[("share/colin/config/", ["config/default.json",
                                         "config/fedora.json",
                                         "config/redhat.json"])],
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Utilities',
    ],
)
