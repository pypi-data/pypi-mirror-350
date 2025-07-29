#!/usr/bin/env python

"""The setup script."""

import pathlib
from os import path

from setuptools import setup, find_namespace_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# automatically captured required modules for install_requires in requirements.txt
# and as well as configure dependency links
HERE = pathlib.Path(__file__).parent
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requirements = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]


test_requirements = []

setup(
    name='PyDeftLariats',
    author="Tyler McMaster",
    author_email='mcmasty@yahoo.com',
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Using PyHamcrest to build a collection of data filters.",
    entry_points={
        'console_scripts': [
            'deft=deftlariat.scripts.cli:deft_cli',
        ],
    },
    install_requires=install_requirements,
    license="GNU General Public License v3",
    keywords="hamcrest matchers data filters",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    package_data={"deftlariat": ["py.typed"]},
    provides=['deftlariat'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mcmasty/PyDeftLariats',
    version='1.2.11',
    zip_safe=False,
)
