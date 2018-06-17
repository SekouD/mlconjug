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
__version__ = '2.1.5'

from .mlconjug import *
from .PyVerbiste import *
import pkg_resources
import platform
import locale
import gettext

__all__ = (mlconjug.__all__ + PyVerbiste.__all__)

# Sets up the automatic translation of annotated strings displayed to the user.
RESOURCE_PACKAGE = __name__
TRANSLATIONS_PATH = pkg_resources.resource_filename(RESOURCE_PACKAGE, 'locale')

SUPPORETD_LANGUAGES = ('es', 'fr', 'it', 'pt', 'ro')

if 'Windows' in platform.system():
    import ctypes
    windll = ctypes.windll.kernel32
    user_locale = locale.windows_locale[ windll.GetUserDefaultUILanguage() ][:2]
else:
    user_locale = locale.getdefaultlocale()[0][:2]

if user_locale in SUPPORETD_LANGUAGES:
    MLCONJUG_TRANSLATIONS = gettext.translation(domain='mlconjug',
                                                localedir=pkg_resources.resource_filename(RESOURCE_PACKAGE, 'locale'),
                                                languages=[user_locale], fallback=True, codeset='UTF-8')
else:
    MLCONJUG_TRANSLATIONS = gettext.NullTranslations()

MLCONJUG_TRANSLATIONS.install()


# Enables the translation of docstrings when using the help() builtin function.
import inspect
def getdoc(object):
    try:
        doc = object.__doc__
    except AttributeError:
        return None
    if not isinstance(doc, str):
        return None
    return inspect.cleandoc(_(doc))

# Replaces the getdoc method
inspect.getdoc = getdoc
