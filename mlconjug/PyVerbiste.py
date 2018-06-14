# -*- coding: utf-8 -*-

"""
PyVerbiste.
A Python library for conjugating verbs.
It uses verbiste xml conjugation data.
Verbiste can be downloaded at https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html

"""

import copy
import xml.etree.ElementTree as ET
import codecs
from collections import OrderedDict
import pkg_resources
from _io import BufferedReader

resource_package = __name__
verbs_resource_path = {'fr': '/'.join(('data', 'verbiste', 'verbs-fr.xml')),
                       'it': '/'.join(('data', 'verbiste', 'verbs-it.xml')),
                       'es': '/'.join(('data', 'verbiste', 'verbs-es.xml')),
                       'en': '/'.join(('data', 'verbiste', 'verbs-en.xml')),
                       'pt': '/'.join(('data', 'verbiste', 'verbs-pt.xml')),
                       'ro': '/'.join(('data', 'verbiste', 'verbs-ro.xml')),}

conjugations_resource_path = {'fr': '/'.join(('data', 'verbiste', 'conjugation-fr.xml')),
                              'it': '/'.join(('data', 'verbiste', 'conjugation-it.xml')),
                              'es': '/'.join(('data', 'verbiste', 'conjugation-es.xml')),
                              'en': '/'.join(('data', 'verbiste', 'conjugation-en.xml')),
                              'pt': '/'.join(('data', 'verbiste', 'conjugation-pt.xml')),
                              'ro': '/'.join(('data', 'verbiste', 'conjugation-ro.xml')),}

pronouns = {'fr': ("je", "tu", "il (elle, on)", "nous", "vous", "ils (elles)"),
            'it': ('io', 'tu', 'egli/ella', 'noi', 'voi', 'essi/esse'),
            'es': ('yo', 'tú', 'él', 'nosotros', 'vosotros', 'ellos'),
            'en': ('I', 'you', 'he/she/it', 'you', 'we', 'they'),
            'pt': ('eu', 'tu', 'ele', 'nós', 'vós', 'eles'),
            'ro': ('eu','tu', 'el/ea', 'noi', 'voi', 'ei/ele')}
persons = ("1s", "2s", "3s", "1p", "2p", "3p")

negation = {'fr': 'ne',
            'it': 'non',
            'es': 'no',
            'en': "don't",
            'pt': 'não',
            'ro': 'nu'}

for key, values in pronouns.items():
    pronouns[key] = OrderedDict(zip(persons, values))
    pass

class Verbiste:
    """
    This is the class handling the Verbiste xml files.

    :param language: string.
        The language of the conjugator. The default value is fr for French.
    :param subject: string.
        Value can be either 'default' or 'pronoun' depending on if you want to have full pronouns or abbreviated pronouns.

    """

    def __init__(self, language='fr', subject='default'):
        self.language = language
        self.subject = subject
        self.verbs = {}
        self.conjugations = OrderedDict()
        verbs_file = pkg_resources.resource_stream(
        resource_package, verbs_resource_path[language])
        self._load_verbs(verbs_file)
        conjugations_file = pkg_resources.resource_stream(
        resource_package, conjugations_resource_path[language])
        self._load_conjugations(conjugations_file)
        self.templates = sorted(self.conjugations.keys())
        self.model = None

    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from xml file.

        :param verbs_path: string or path object.
            Path to the verbs xml file.
        """
        verbs_dic = {}
        if isinstance(verbs_file, BufferedReader):
            verbs_dic = self._parse_verbs(verbs_file)
        else:
            with codecs.open(verbs_file, "r", encoding='utf-8') as file:
                verbs_dic = self._parse_verbs(file)
        self.verbs = verbs_dic

    def _parse_verbs(self, file):
        """
        Parses XML file

        :param file: XML file containing the verbs.
        :return: OrderedDict.
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
        Load and parses the conjugations from xml file.

        :param conjugations_path: string or path object.
            Path to the conjugation xml file.
        """
        if isinstance(conjugations_file, BufferedReader):
            conjugations_dic = self._parse_conjugations(conjugations_file)
        else:
            with codecs.open(conjugations_file, "r", encoding='utf-8') as file:
                conjugations_dic = self._parse_conjugations(file)
        self.conjugations = conjugations_dic

    def _parse_conjugations(self, file):
        """
        Parses XML file

        :param file: XML file containing the conjugation templates
        :return: OrderedDict
        """
        conjugations_dic = {}
        xml = ET.parse(file)
        for template in xml.findall("template"):
            template_name = template.get("name")
            conjugations_dic[template_name] = OrderedDict()
            for mood in list(template):
                conjugations_dic[template_name][mood.tag] = OrderedDict()
                for tense in list(mood):
                    conjugations_dic[template_name][mood.tag][tense.tag] = self._load_tense(mood, tense)
        return conjugations_dic


    def _load_tense(self, mood, tense):
        persons = list(tense)
        if len(persons) == 1:
            if persons[0].find("i") is not None:
                conjug = persons[0].find("i").text
            else:
                conjug = None
        elif len(persons) == 6 and not mood.tag.startswith('Imperativ'):
            conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
                                                               not None else None) for pers, term in
                                 zip(pronouns[self.language], persons))
        elif len(persons) == 6 and mood.tag.startswith('Imperativ'):
            if 'Negativo' in tense.tag or 'non' in tense.tag:
                conjug = OrderedDict(((negation[self.language], term.find("i").text) if term.find("i") is not None else None for term in persons))
            else:
                conjug = OrderedDict(((i, term.find("i").text) if term.find("i") is not None else None for i, term in
                                      enumerate(persons)))
        elif len(persons) == 5 and mood.tag.startswith('Imperativ'):
            if 'Negativo' in tense.tag or 'non' in tense.tag:
                conjug = OrderedDict(
                    ((negation[self.language], term.find("i").text) if term.find("i") is not None else None for term in
                     persons))
            else:
                conjug = OrderedDict(((i, term.find("i").text) if term.find("i") is not None else None for i, term in enumerate(persons)))
        else:
            try:
                conjug = OrderedDict(((i, term.find("i").text) if term.text is not None and term.find("i") is not None else None for i, term in enumerate(persons)))
            except TypeError:
                conjug = [(i, term.find("i").text) if term.text is not None and term.find("i") is not None else None for i, term in enumerate(persons)]
        return conjug




    # def _load_tense(self, mood, tense):
    #     """
    #     Parses XML objects and extract mood and tense information to create a dict containing all inflected forms of the verb.
    #
    #     :param mood: xml.etree.ElementTree Tag object.
    #     :param tense: xml.etree.ElementTree Tag object.
    #     :return: OrderedDict or None.
    #     """
    #     # TODO: add pronouns for languages other than french.
    #     persons = list(tense)
    #     if tense.tag in ('infinitive-present', 'present-participle'):
    #         if persons[0].find("i") is not None:
    #             conjug = persons[0].find("i").text
    #         else:
    #             conjug = None
    #     elif tense.tag == 'imperative-present':
    #         pronouns = ["2s :", "1p :", "2p :"]
    #         conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
    #                                                            not None else None) for pers, term in
    #                              zip(pronouns, persons))
    #     elif tense.tag == 'past-participle':
    #         pronouns = ["ms :", "mp :", "fs :", "fp :"]
    #         conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
    #                                                            not None else None) for pers, term in
    #                              zip(pronouns, persons))
    #     elif len(persons) == 6:
    #         if self.subject == 'pronoun':
    #             pronouns = ["je", "tu", "il (elle, on)", "nous", "vous", "ils (elles)"]
    #             if mood.tag == 'subjunctive':
    #                 prefix1 = "que "
    #                 prefix2 = "qu' "
    #                 exceptions = ("il (elle, on)", "ils (elles)")
    #                 pronouns = [prefix1 + elmt if elmt not in exceptions else prefix2 + elmt for elmt in pronouns]
    #         else:
    #             pronouns = ["1s", "2s", "3s", "1p", "2p", "3p"]
    #         conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
    #                                                            not None else None) for pers, term in
    #                              zip(pronouns, persons))
    #     return conjug

    def get_verb_info(self, verb):
        """
        Gets verb information and returns a VerbInfo instance.

        :param verb: string.
            Verb to conjugate.
        :return: VerbInfo object or None.
        """
        if verb not in self.verbs.keys():
            return None
        else:
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
        """
        if template not in self.conjugations.keys():
            return None
        else:
            info = copy.deepcopy(self.conjugations[template])
            return info


class VerbInfo(object):
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
        self.root = root
        self.template = template

    def __eq__(self, other):
        if self.infinitive == other.infinitive \
            and self.root == other.root \
            and self.root == other.root:
            return True
        else:
            return False


class Verb(object):
    """
    This class defines the Verb Object.

    :param verb_info: VerbInfo Object.
    :param conjug_info: OrderedDict.

    """
    __slots__ = ('name', 'verb_info', 'conjug_info')

    def __init__(self, verb_info, conjug_info):
        self.name = verb_info.infinitive
        self.verb_info = verb_info
        self.conjug_info = conjug_info
        self._load_conjug()

    def _load_conjug(self):
        """
        Populates the inflected forms of the verb.

        """
        for mood, tense in self.conjug_info.items():
            for tense, persons in tense.items():
                if isinstance(persons, dict):
                    for pers, term in persons.items():
                        if term is not None:
                            persons[pers] = self.verb_info.root + term
                        else:
                            persons[pers] = None
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense] = self.verb_info.root + persons
                    pass


if __name__ == "__main__":
    # verbiste_fr = Verbiste('fr')
    # verbiste_it = Verbiste('it')
    # verbiste_es = Verbiste('es')
    # verbiste_en = Verbiste('en')
    # verbiste_pt = Verbiste('pt')
    # verbiste_ro = Verbiste('ro')
    pass
