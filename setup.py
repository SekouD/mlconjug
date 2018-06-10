#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'numpy==1.14.3',
    'scipy==1.1.0',
    'scikit-learn==0.19.',
]

setup_requirements = [
    'pytest-runner',
    # TODO(SekouD): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    'Sphinx',
    'docutils',
    'pytest',
    'pytest-cov',
    'Click>=6.0',
    'lxml',
]

setup(
    name='mlconjug',
    version='1.0.0',
    description="A Python library to conjugate verbs using Machine Learning techiques.",
    long_description=readme + '\n\n' + history,
    author="SekouD",
    author_email='sekoud.python@gmail.com',
    url='https://github.com/SekouD/mlconjug',
    packages=find_packages(include=['mlconjug']),
    entry_points={
        'console_scripts': [
            'mlconjug=mlconjug.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mlconjug',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: French',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
