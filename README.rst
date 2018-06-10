========
MLConjug
========


.. image:: https://img.shields.io/pypi/v/mlconjug.svg
        :target: https://pypi.python.org/pypi/mlconjug
        :alt: Pypi Python Package Index Status

.. image:: https://img.shields.io/travis/SekouD/mlconjug.svg
        :target: https://travis-ci.org/SekouD/mlconjug
        :alt: Linux Continuous Integration Status

.. image:: https://ci.appveyor.com/api/projects/status/6iatj101xxfehbo8/branch/master?svg=true
        :target: https://ci.appveyor.com/project/SekouD/mlconjug
        :alt: Windows Continuous Integration Status

.. image:: https://readthedocs.org/projects/mlconjug/badge/?version=latest
        :target: https://mlconjug.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/SekouD/mlconjug/shield.svg
        :target: https://pyup.io/repos/github/SekouD/mlconjug/
        :alt: Depedencies Update Status

.. image:: https://codecov.io/gh/SekouD/mlconjug/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/SekouD/mlconjug
        :alt: Coverage Status


A Python library to conjugate verbs of Romance languages using Machine Learning techniques.
Any verb in one of the supported language can be conjugated as the module contains a Machine Learning model of how romance verbs behave.
Even completely new or made-up verbs can be successfully conjugated in this manner.
The supplied pre-trained models are composed of:

- a binary feature extractor,
- a feature selector using Linear Support Vector Classification,
- a classifier using Stochastic Gradient Descent.

MLConjug uses scikit-learn to implement the Machine Learning algorithms.
Users of the library can use any compatible classifiers from scikit-learn to modify and retrain the model.

The training data is based on Verbiste https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html .


* Free software: MIT license
* Documentation: https://mlconjug.readthedocs.io.

Supported Languages
-------------------

- French
- Spanish (coming in next update)
- Italian (coming in next update)
- Portuguese (coming in next update)


Features
--------

- Easy to use API.
- Includes a pre-trained model with 99.53% accuracy in predicting conjugation class of unknown verbs.
- Easily train new models or add new romance language.
- Easily integrate MLConjug in your own projects.
- Can be used as a command line tool.

Credits
---------

This package was created with the help of Verbiste_ and scikit-learn_.

.. _Verbiste: https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html
.. _scikit-learn: http://scikit-learn.org/stable/index.html

