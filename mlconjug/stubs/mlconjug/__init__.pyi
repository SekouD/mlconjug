# Stubs for mlconjug (Python 3.6)


from .mlconjug import *
from .PyVerbiste import *
from typing import Any, Text, Tuple, Dict
import gettext

__author__: Text
__email__: Text
__version__: Text
_RESOURCE_PACKAGE: Text = __name__
_TRANSLATIONS_PATH: Text
_SUPPORTED_LANGUAGES: Tuple[Text]
_TRANSLATED_LANGUAGES: Tuple[Text]
windows_locale: Dict[int, Text]
_user_locale: Text
_MLCONJUG_TRANSLATIONS: gettext.GNUTranslations

def _get_user_locale() -> Text: ...

def getdoc(object: Text): ...
