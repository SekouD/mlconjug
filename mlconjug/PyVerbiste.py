# -*- coding: utf-8 -*-

"""
PyVerbiste.

| A Python library for conjugating verbs in French, English, Spanish, Italian, Portuguese and Romanian (more soon).
| It contains conjugation data generated by machine learning models using the python library mlconjug.
| More information about mlconjug at https://pypi.org/project/mlconjug/


| The conjugation data conforms to the XML schema defined by Verbiste.
| More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""

__author__ = 'SekouD'
__author_email__ = 'sekoud.python@gmail.com'


import copy
import xml.etree.ElementTree as ET
import json
from collections import OrderedDict
import pkg_resources


_RESOURCE_PACKAGE = __name__

_LANGUAGES = ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro')

_VERBS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'verbs-fr.json')),
                        'it': '/'.join(('data', 'conjug_manager', 'verbs-it.json')),
                        'es': '/'.join(('data', 'conjug_manager', 'verbs-es.json')),
                        'en': '/'.join(('data', 'conjug_manager', 'verbs-en.json')),
                        'pt': '/'.join(('data', 'conjug_manager', 'verbs-pt.json')),
                        'ro': '/'.join(('data', 'conjug_manager', 'verbs-ro.json')),}

_CONJUGATIONS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'conjugation-fr.json')),
                               'it': '/'.join(('data', 'conjug_manager', 'conjugation-it.json')),
                               'es': '/'.join(('data', 'conjug_manager', 'conjugation-es.json')),
                               'en': '/'.join(('data', 'conjug_manager', 'conjugation-en.json')),
                               'pt': '/'.join(('data', 'conjug_manager', 'conjugation-pt.json')),
                               'ro': '/'.join(('data', 'conjug_manager', 'conjugation-ro.json')),}

_ABBREVS = ("1s", "2s", "3s", "1p", "2p", "3p")

_PRONOUNS = {'fr': {'abbrev': _ABBREVS,
                   'pronoun': ("je", "tu", "il (elle, on)", "nous", "vous", "ils (elles)")},
             'it': {'abbrev': _ABBREVS,
                   'pronoun': ('io', 'tu', 'egli/ella', 'noi', 'voi', 'essi/esse')},
             'es': {'abbrev': _ABBREVS,
                   'pronoun': ('yo', 'tú', 'él', 'nosotros', 'vosotros', 'ellos')},
             'en': {'abbrev': _ABBREVS,
                   'pronoun': ('I', 'you', 'he/she/it', 'you', 'we', 'they')},
             'pt': {'abbrev': _ABBREVS,
                   'pronoun': ('eu', 'tu', 'ele', 'nós', 'vós', 'eles')},
             'ro': {'abbrev': _ABBREVS,
                   'pronoun': ('eu', 'tu', 'el/ea', 'noi', 'voi', 'ei/ele')}
             }

_IMPERATIVE_PRONOUNS = {'fr': {'abbrev': ("2s", "1p", "2p"),
                              'pronoun': ("", "", "")},
                        'it': None,
                        'es': {'abbrev': ("2s", "3s", "1p", "2p", "3p"),
                              'pronoun': ('tú', 'él', 'nosotros', 'vosotros', 'ellos')},
                        'en': {'abbrev': ("2s", "1p", "2p"),
                              'pronoun': ("", "let's", "")},
                        'pt': None,
                        'ro': {'abbrev': ("2s", "2p"),
                              'pronoun': ("tu", "voi")},
                        }

_AUXILIARIES = {'fr':None,
                'it': 'non',
                'es': 'no',
                'en':  {'abbrev': _ABBREVS,
                    'pronoun': ('am', 'are', 'is', 'are', 'are', 'are')},
                'pt': 'não',
                'ro': 'nu'}

_GENDER = {'fr': {'abbrev': ("ms", "mp", "fs", "fp"),
                 'pronoun': ("masculin singulier", "masculin pluriel", "feminin singulier", "feminin pluriel")},
           'it': None,
           'es': None,
           'en': None,
           'pt': None,
           'ro': None}

_NEGATION = {'fr': 'ne',
             'it': 'non',
             'es': 'no',
             'en': "don't",
             'pt': 'não',
             'ro': 'nu'}


class ConjugManager:
    """
        This is the class handling the mlconjug json files.

        :param language: string.
            | The language of the conjugator. The default value is fr for French.
            | The allowed values are: fr, en, es, it, pt, ro.

        """

    def __init__(self, language='default'):
        if language not in _LANGUAGES:
            raise ValueError(_('Unsupported language.\nThe allowed languages are fr, en, es, it, pt, ro.'))
        if language == 'default':
            self.language = 'fr'
        else:
            self.language = language
        self.verbs = {}
        self.conjugations = OrderedDict()
        verbs_file = pkg_resources.resource_filename(_RESOURCE_PACKAGE, _VERBS_RESOURCE_PATH[self.language])
        self._load_verbs(verbs_file)
        self._allowed_endings = self._detect_allowed_endings()
        conjugations_file = pkg_resources.resource_filename(_RESOURCE_PACKAGE,
                                                            _CONJUGATIONS_RESOURCE_PATH[self.language])
        self._load_conjugations(conjugations_file)
        self.templates = sorted(self.conjugations.keys())
        return

    def __repr__(self):
        return '{0}.{1}(language={2})'.format(__name__, self.__class__.__name__, self.language)

    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from the json file.

        :param verbs_file: string or path object.
            Path to the verbs json file.

        """
        with open(verbs_file, 'r', encoding='utf-8') as file:
            self.verbs = json.load(file)
        return

    def _load_conjugations(self, conjugations_file):
        """
        Load and parses the conjugations from the xml file.

        :param conjugations_file: string or path object.
            Path to the conjugation xml file.

        """
        with open(conjugations_file, 'r', encoding='utf-8') as file:
            self.conjugations = json.load(file)
        return

    def _detect_allowed_endings(self):
        """
        | Detects the allowed endings for verbs in the supported languages.
        | All the supported languages except for English restrict the form a verb can take.
        | As English is much more productive and varied in the morphology of its verbs, any word is allowed as a verb.

        :return: set.
            A set containing the allowed endings of verbs in the target language.

        """
        if self.language == 'en':
            return True
        results = {verb.split(' ')[0][-2:] for verb in self.verbs if 2 <= len(verb)}
        return results

    def is_valid_verb(self, verb):
        """
        | Checks if the verb is a valid verb in the given language.
        | English words are always treated as possible verbs.
        | Verbs in other languages are filtered by their endings.

        :param verb: string.
            The verb to conjugate.
        :return: bool.
            True if the verb is a valid verb in the language. False otherwise.

        """
        if self.language == 'en':
            return True  # LOL!
        if verb[-2:] in self._allowed_endings:
            return True
        else:
            return False

    def get_verb_info(self, verb):
        """
        Gets verb information and returns a VerbInfo instance.

        :param verb: string.
            Verb to conjugate.
        :return: VerbInfo object or None.

        """
        if verb not in self.verbs.keys():
            return None
        infinitive = verb
        root = self.verbs[verb]['root']
        template = self.verbs[verb]['template']
        verb_info = VerbInfo(infinitive, root, template)
        return verb_info

    def get_conjug_info(self, template):
        """
        Gets conjugation information corresponding to the given template.

        :param template: string.
            Name of the verb ending pattern.
        :return: OrderedDict or None.
            OrderedDict containing the conjugated suffixes of the template.

        """
        if template not in self.conjugations.keys():
            return None
        info = copy.deepcopy(self.conjugations[template])
        return info


class Verbiste(ConjugManager):
    """
    This is the class handling the Verbiste xml files.

    :param language: string.
        | The language of the conjugator. The default value is fr for French.
        | The allowed values are: fr, en, es, it, pt, ro.

    """

    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from the xml file.

        :param verbs_file: string or path object.
            Path to the verbs xml file.

        """
        self.verbs = self._parse_verbs(verbs_file.replace('json', 'xml'))
        return

    def _parse_verbs(self, file):
        """
        Parses the XML file.

        :param file: FileObject.
            XML file containing the verbs.
        :return: OrderedDict.
            An OrderedDict containing the verb and its template for all verbs in the file.

        """
        verbs_dic = {}
        xml = ET.parse(file)
        for verb in xml.findall("v"):
            verb_name = verb.find("i").text
            template = verb.find("t").text
            index = - len(template[template.index(":") + 1:])
            root = verb_name[:index]
            verbs_dic[verb_name] = {"template": template, "root": root}
        return verbs_dic

    def _load_conjugations(self, conjugations_file):
        """
        Load and parses the conjugations from the xml file.

        :param conjugations_file: string or path object.
            Path to the conjugation xml file.

        """
        self.conjugations = self._parse_conjugations(conjugations_file.replace('json', 'xml'))
        return

    def _parse_conjugations(self, file):
        """
        Parses the XML file.

        :param file: FileObject.
            XML file containing the conjugation templates.
        :return: OrderedDict.
            An OrderedDict containing all the conjugation templates in the file.

        """
        conjugations_dic = {}
        xml = ET.parse(file)
        for template in xml.findall("template"):
            template_name = template.get("name")
            conjugations_dic[template_name] = OrderedDict()
            for mood in list(template):
                conjugations_dic[template_name][mood.tag] = OrderedDict()
                for tense in list(mood):
                    conjugations_dic[template_name][mood.tag][tense.tag.replace('-', ' ')] = self._load_tense(tense)
        return conjugations_dic

    def _load_tense(self, tense):
        """
        Load and parses the inflected forms of the tense from xml file.

        :param tense: list of xml tags containing inflected forms.
            The list of inflected forms for the current tense being processed.
        :return: list.
            List of inflected forms.

        """
        persons = list(tense)
        if not persons:
            return None
        elif len(persons) == 1:
            if persons[0].find("i") is None:
                return None
            conjug = persons[0].find("i").text
        else:
            conjug = [(pers, term.find("i").text if term.find("i") is not None else None)
                      for pers, term in enumerate(persons)]
        return conjug


class VerbInfo:
    """
    This class defines the Verbiste verb information structure.

    :param infinitive: string.
        Infinitive form of the verb.
    :param root: string.
        Lexical root of the verb.
    :param template: string.
        Name of the verb ending pattern.

    """
    __slots__ = ('infinitive', 'root', 'template')

    def __init__(self, infinitive, root, template):
        self.infinitive = infinitive
        if not root:
            self.root = infinitive
        else:
            self.root = root
        self.template = template
        return

    def __repr__(self):
        return '{0}.{1}({2}, {3}, {4})'.format(__name__, self.__class__.__name__, self.infinitive, self.root, self.template)

    def __eq__(self, other):
        if not isinstance(other, VerbInfo):
            return NotImplemented
        return self.infinitive == other.infinitive and self.root == other.root and self.template == other.template


class Verb:
    """
    This class defines the Verb Object.

    :param verb_info: VerbInfo Object.
    :param conjug_info: OrderedDict.
    :param subject: string.
        Toggles abbreviated or full pronouns.
        The default value is 'abbrev'.
        Select 'pronoun' for full pronouns.
    :param predicted: bool.
        Indicates if the conjugation information was predicted by the model or retrieved from the dataset.

    """
    __slots__ = ('name', 'verb_info', 'conjug_info', 'subject', 'predicted', 'confidence_score')

    language = 'default'

    def __init__(self, verb_info, conjug_info, subject='abbrev', predicted=False):
        self.name = verb_info.infinitive
        self.verb_info = verb_info
        self.conjug_info = conjug_info
        self.subject = subject
        self.predicted = predicted
        self.confidence_score = None
        self._load_conjug()
        return

    def __repr__(self):
        return '{0}.{1}({2})'.format(__name__, self.__class__.__name__, self.name)

    def _load_conjug(self):
        """
        | Populates the inflected forms of the verb.
        | This is the generic version of this method.
        | It does not add personal pronouns to the conjugated forms.
        | This method can handle any new language if the conjugation structure conforms to the Verbiste XML Schema.

        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6:
                            key = _ABBREVS[pers]
                        else:
                            key = ''
                        if term is not None:
                            persons_dict[key] = self.verb_info.root + term
                        else:
                            persons[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbFr(Verb):
    """
    This class defines the French Verb Object.

    """
    __slots__ = ()

    language = 'fr'

    def _load_conjug(self):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.

        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6:
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Participe Passé':
                            key = _GENDER[self.language][self.subject][pers]
                        elif tense_name == 'Imperatif Présent':
                            key = _IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                        else:
                            key = term
                        if term is not None:
                            persons_dict[key] = self.verb_info.root + term
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbEn(Verb):
    """
    This class defines the English Verb Object.

    """
    __slots__ = ()

    language = 'en'

    def _load_conjug(self):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.

        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if tense_name == 'indicative present continuous':
                            key = " ".join((_PRONOUNS[self.language][self.subject][pers],
                                            _AUXILIARIES[self.language][self.subject][pers],))
                            pass
                        elif len(persons) == 6 and not tense_name == 'indicative present continuous':
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'imperative present':
                            key = _IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                        else:
                            key = term
                        if term is not None:
                            persons_dict[key] = self.verb_info.root + term
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    if tense_name == 'infinitive present':
                        prefix = 'to '
                    else:
                        prefix = ''
                    self.conjug_info[mood][tense_name] = prefix + self.verb_info.root + persons
        return


class VerbEs(Verb):
    """
    This class defines the Spanish Verb Object.

    """
    __slots__ = ()

    language = 'es'

    def _load_conjug(self):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.

        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6:
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativo Afirmativo':
                            key = _IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativo non':
                            key = ' '.join((_IMPERATIVE_PRONOUNS[self.language][self.subject][pers],
                                            _NEGATION[self.language]))
                        else:
                            key = ''
                        if term is not None:
                            persons_dict[key] = self.verb_info.root + term
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbIt(Verb):
    """
    This class defines the Italian Verb Object.

    """
    __slots__ = ()

    language = 'it'

    def _load_conjug(self):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.

        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6 and not tense_name.startswith('Imperativo'):
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativo Imperativo':
                            key = ''
                        elif tense_name == 'Imperativo non':
                            key = _NEGATION[self.language]
                        else:
                            key = ''
                        if term is not None:
                            persons_dict[key] = self.verb_info.root + term
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbPt(Verb):
    """
    This class defines the Portuguese Verb Object.

    """
    __slots__ = ()

    language = 'pt'

    def _load_conjug(self):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.

        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6 and not tense_name.startswith('Imperativo'):
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativo Afirmativo':
                            key = ''
                        elif tense_name == 'Imperativo Negativo':
                            key = _NEGATION[self.language]
                        else:
                            key = ''
                        if term is not None:
                            persons_dict[key] = self.verb_info.root + term
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbRo(Verb):
    """
    This class defines the Romanian Verb Object.

    """
    __slots__ = ()

    language = 'ro'

    def _load_conjug(self):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.

        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6:
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativ Imperativ':
                            key = _IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                            # key = pers
                            pass
                        elif tense_name == 'Imperativ Negativ':
                            key = _NEGATION[self.language]
                        else:
                            key = ''
                        if term is not None:
                            persons_dict[key] = self.verb_info.root + term
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    if tense_name == 'Infinitiv Infinitiv':
                        prefix = 'a '
                    else:
                        prefix = ''
                    self.conjug_info[mood][tense_name] = prefix + self.verb_info.root + persons
        return


if __name__ == "__main__":
    pass
