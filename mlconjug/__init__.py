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


| MIT License

| Copyright (c) 2017, SekouD

| Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

| The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""

__author__ = """SekouD"""
__email__ = 'sekoud.python@gmail.com'
__version__ = '2.1.6'

from .mlconjug import *
from .PyVerbiste import *
import pkg_resources
import platform
from locale import windows_locale, getdefaultlocale
import gettext
import inspect

# Sets up the automatic translation of annotated strings displayed to the user.
_RESOURCE_PACKAGE = __name__
_TRANSLATIONS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'locale')

_SUPPORTED_LANGUAGES = ('default', 'en', 'es', 'fr', 'it', 'pt', 'ro')
_TRANSLATED_LANGUAGES = _SUPPORTED_LANGUAGES[2:]


def _get_user_locale():
    """
    | Gets the user locale to set the user interface language language.
    | The default is set to english if the user's system locale is not one of the translated languages.

    :return: string.
        The user locale.

    """
    if 'Windows' in platform.system():
        import ctypes
        windll = ctypes.windll.kernel32
        default_locale = windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        default_locale = getdefaultlocale()
    if default_locale:
        if isinstance(default_locale, tuple):
            user_locale = [0][:2]
        else:
            user_locale = default_locale[:2]
    else:
        user_locale = 'en'
    return user_locale


def getdoc(object):
    """
    Translates the docstrings of the objects defined in the packeage in the supported languages.

    :param object:
    :return: string.
        The translated version of the object's docstring.
    """
    try:
        doc = object.__doc__
    except AttributeError:
        return None
    if not isinstance(doc, str):
        return None
    return inspect.cleandoc(_(doc))


_user_locale = _get_user_locale()

if _user_locale in _TRANSLATED_LANGUAGES:
    _MLCONJUG_TRANSLATIONS = gettext.translation(domain='mlconjug',
                                                localedir=_TRANSLATIONS_PATH,
                                                languages=[_user_locale], fallback=True, codeset='UTF-8')
else:
    _MLCONJUG_TRANSLATIONS = gettext.NullTranslations()

_MLCONJUG_TRANSLATIONS.install()


# Replaces the getdoc method
inspect.getdoc = getdoc
