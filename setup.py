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
    version='1.2.1',
    description="A Python library to conjugate French (and many other Romance languages) verbs using Machine Learning techniques.",
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
    package_data={'verbiste_data': ['mlconjug/data/verbiste/*'],
                  'trained_models': 'mlconjug/data/models/*'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mlconjug conjugation conjugaison verbs verbes ML machine learning NLP verbiste sklearn',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: Spanish',
        'Natural Language :: Italian',
        'Natural Language :: Portuguese',
        'Operating System :: OS Independent',
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
