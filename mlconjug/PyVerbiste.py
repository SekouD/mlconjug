# -*- coding: utf-8 -*-

"""
PyVerbiste.
A Python library for conjugating verbs.
It uses verbiste xml conjugation data.
Verbiste can be downloaded at https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html

"""

import xml.etree.ElementTree as ET
import codecs
from collections import OrderedDict


class Verbiste:
    """
    This is the class handling the Verbiste xml files.

    :param verbs_path: string or path object.
        Path to the verbs xml file.
    :param conjugations_path: string or path object.
        Path to the conjugation xml file.
    :param subject: string.
        Value can be either 'default' or 'pronoun' depending on if you want to have full pronouns or abbreviated pronouns.

    """

    def __init__(self, verbs_path, conjugations_path, subject='default'):
        self.subject = subject
        self.verbs = {}
        self.conjugations = OrderedDict()
        self._load_verbs(verbs_path)
        self._load_conjugations(conjugations_path)
        self.templates = sorted(self.conjugations.keys())
        self.model = None

    def _load_verbs(self, verbs_path):
        """
        Load and parses the verbs from xml file.

        :param verbs_path: string or path object.
            Path to the verbs xml file.
        """
        verbs_dic = {}
        with codecs.open(verbs_path, "r", encoding='utf-8') as file:
            xml = ET.parse(file)
            for verb in xml.findall("v"):
                verb_name = verb.find("i").text
                template = verb.find("t").text
                index = - len(template[template.index(":") + 1:])
                root = verb_name[:index]
                verbs_dic[verb_name] = {"template": template, "root": root}
        self.verbs = verbs_dic

    def _load_conjugations(self, conjugations_path):
        """
        Load and parses the conjugations from xml file.

        :param conjugations_path: string or path object.
            Path to the conjugation xml file.
        """
        conjugations_dic = {}
        with codecs.open(conjugations_path, "r", encoding='utf-8') as file:
            xml = ET.parse(file)
            for template in xml.findall("template"):
                template_name = template.get("name")
                conjugations_dic[template_name] = OrderedDict()
                for mood in list(template):
                    conjugations_dic[template_name][mood.tag] = OrderedDict()
                    for tense in list(mood):
                        conjugations_dic[template_name][mood.tag][tense.tag] = self._load_tense(mood, tense)
        self.conjugations = conjugations_dic

    def _load_tense(self, mood, tense):
        """
        Parses XML objects and extract mood and tense information to create a dict containing all inflected forms of the verb.

        :param mood: xml.etree.ElementTree Tag object.
        :param tense: xml.etree.ElementTree Tag object.
        :return: OrderedDict or None.
        """
        persons = list(tense)
        if tense.tag in ('infinitive-present', 'present-participle'):
            if persons[0].find("i") is not None:
                conjug = persons[0].find("i").text
            else:
                conjug = None
        elif tense.tag == 'imperative-present':
            pronouns = ["2s :", "1p :", "2p :"]
            conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
                                                               not None else None) for pers, term in
                                 zip(pronouns, persons))
        elif tense.tag == 'past-participle':
            pronouns = ["ms :", "mp :", "fs :", "fp :"]
            conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
                                                               not None else None) for pers, term in
                                 zip(pronouns, persons))
        elif len(persons) == 6:
            if self.subject == 'pronoun':
                pronouns = ["je", "tu", "il (elle, on)", "nous", "vous", "ils (elles)"]
                if mood.tag == 'subjunctive':
                    prefix1 = "que "
                    prefix2 = "qu' "
                    exceptions = ("il (elle, on)", "ils (elles)")
                    pronouns = [prefix1 + elmt if elmt not in exceptions else prefix2 + elmt for elmt in pronouns]
            else:
                pronouns = ["1s", "2s", "3s", "1p", "2p", "3p"]
            conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
                                                               not None else None) for pers, term in
                                 zip(pronouns, persons))
        return conjug

    def _get_verb_info(self, verb):
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

    def _get_conjug_info(self, template):
        """
        Gets conjugation information corresponding to the given template.

        :param template: string.
            Name of the verb ending pattern.
        :return: OrderedDict or None.
        """
        if template not in self.conjugations.keys():
            return None
        else:
            return self.conjugations[template]

    def conjugate(self, verb):
        """
        This is the main method of this class.
        It first checks to see if the verb is in Verbiste. If it is not, and a pre-trained scikit-learn model has been supplied,
        the method then calls the model to predict the conjugation class of the provided verb.
        Returns a Verb object.

        :param verb: string.
            Verb to conjugate.
        :return verb_object: Verb object or None.
        """
        infinitive = None
        if verb not in self.verbs.keys():
            if self.model is None:
                return None
            predicted = self.model.predict([verb])[0]
            template = self.templates[predicted]
            index = - len(template[template.index(":") + 1:])
            root = verb[:index]
            verb_info = VerbInfo(verb, root, template)
            conjug_info = self._get_conjug_info(verb_info.template)
        else:
            infinitive = verb
            verb_info = self._get_verb_info(infinitive)
            if verb_info is None:
                return None
            conjug_info = self._get_conjug_info(verb_info.template)
            if conjug_info is None:
                return None
        verb_object = Verb(verb_info, conjug_info)
        return verb_object

    def set_model(self, model):
        """
        Assigns the provided pre-trained scikit-learn model to be able to conjugate unknown verbs.

        :param model: scikit-learn Classifier or Pipeline.
        :return:
        """
        self.model = model
        return


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
    pass
