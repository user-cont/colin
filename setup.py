#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os

from setuptools import find_packages, setup

BASE_PATH = os.path.dirname(__file__)

# https://packaging.python.org/guides/single-sourcing-package-version/
version = {}
with open("./colin/version.py") as fp:
    exec(fp.read(), version)

long_description = ''.join(open('README.md').readlines())

setup(
    name='colin',
    version=version["__version__"],
    description="Tool to check generic rules/best-practices for containers/images/dockerfiles.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['examples', 'tests']),
    install_requires=[
        'Click',
        'six',
        'dockerfile_parse',
        'fmf',
        'PyYAML'
    ],
    entry_points='''
        [console_scripts]
        colin=colin.cli.colin:cli
    ''',
    data_files=[("share/colin/rulesets/", ["rulesets/default.json",
                                           "rulesets/fedora.json"]),
                ("share/bash-completion/completions/", ["bash-complete/colin"])],
    license='GPLv3+',
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Utilities',
    ],
    keywords='containers,sanity,linter',
    author='Red Hat',
    author_email='user-cont-team@redhat.com',
    url='https://github.com/user-cont/colin',
    package_data={'': ['*.fmf']},
    include_package_data=True,
)
