#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='azure_webapp_publish',
    version='0.1.0',
    description="Tool to publish a Python WebApp to Azure easily",
    long_description=readme + '\n\n' + history,
    author="Microsoft Corporation",
    author_email='ptvshelp@microsoft.com',
    url='https://github.com/lmazuel/azure_webapp_publish',
    packages=[
        'azure_webapp_publish',
    ],
    package_dir={'azure_webapp_publish':
                 'azure_webapp_publish'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='azure_webapp_publish',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
