# -*- coding: utf-8 -*-

"""
MLConjug.

A Python library to conjugate verbs of in French, English, Spanish, Italian, Portuguese and Romanian (mores soon) using Machine Learning techniques.
Any verb in one of the supported language can be conjugated as the module contains a Machine Learning model of how the verbs behave.
Even completely new or made-up verbs can be successfully conjugated in this manner.
The supplied pre-trained models are composed of:

- a binary feature extractor,
- a feature selector using Linear Support Vector Classification,
- a classifier using Stochastic Gradient Descent.

MLConjug uses scikit-learn to implement the Machine Learning algorithms.
Users of the library can use any compatible classifiers from scikit-learn to modify and retrain the model.

Usage example:
    $ mlconjug manger

    $ mlconjug bring -l en

    $ mlconjug gallofar --language es
"""

__author__ = """SekouD"""
__email__ = 'sekoud.python@gmail.com'
__version__ = '2.1.2'

from .mlconjug import EndingCountVectorizer, DataSet, Model, LinearSVC, SGDClassifier, SelectFromModel, precision_recall_fscore_support, Conjugator, Pipeline
from .PyVerbiste import Verbiste
