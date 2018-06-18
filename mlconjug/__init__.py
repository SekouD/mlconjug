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

# Sets up the automatic translation of annotated strings displayed to the user.
_RESOURCE_PACKAGE = __name__
_TRANSLATIONS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'locale')

_SUPPORTED_LANGUAGES = ('default', 'en', 'es', 'fr', 'it', 'pt', 'ro')
_TRANSLATED_LANGUAGES = _SUPPORTED_LANGUAGES[2:]


if 'Windows' in platform.system():
    import ctypes
    _windll = ctypes.windll.kernel32
    _user_locale = locale.windows_locale[ _windll.GetUserDefaultUILanguage() ][:2]
else:
    _user_locale = locale.getdefaultlocale()[0][:2]

if _user_locale in _TRANSLATED_LANGUAGES:
    _MLCONJUG_TRANSLATIONS = gettext.translation(domain='mlconjug',
                                                localedir=_TRANSLATIONS_PATH,
                                                languages=[_user_locale], fallback=True, codeset='UTF-8')
else:
    _MLCONJUG_TRANSLATIONS = gettext.NullTranslations()

_MLCONJUG_TRANSLATIONS.install()


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
