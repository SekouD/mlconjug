# -*- coding: utf-8 -*-

"""PyVerbiste.
A Python library for conjugating verbs.
It uses verbiste conjugation data.
https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html

"""


import xml.etree.ElementTree as ET
import codecs
from collections import OrderedDict


class Verbiste:

    def __init__(self, verbs_path, conjugations_path, subject='default'):
        """

        :param verbs_path:
        :param conjugations_path:
        :return:
        """
        self.subject = subject
        self.verbs = {}
        self.conjugations = OrderedDict()
        self.load_verbs(verbs_path)
        self.load_conjugations(conjugations_path)
        self.templates = sorted(self.conjugations.keys())
        self.model = None

    def load_verbs(self, verbs_path):
        """


        """
        verbs_dic = {}
        with codecs.open(verbs_path, "r") as file:
            xml = ET.parse(file)
            for verb in xml.findall("v"):
                verb_name = verb.find("i").text
                template = verb.find("t").text
                index = - len(template[template.index(":") + 1:])
                root = verb_name[:index]
                verbs_dic[verb_name] = {"template": template, "root": root}
        self.verbs = verbs_dic

    def load_conjugations(self, conjugations_path):
        """


        """
        conjugations_dic = {}
        with codecs.open(conjugations_path, "r") as file:
            xml = ET.parse(file)
            for template in xml.findall("template"):
                template_name = template.get("name")
                conjugations_dic[template_name] = OrderedDict()
                for mood in list(template):
                    conjugations_dic[template_name][mood.tag] = OrderedDict()
                    for tense in list(mood):
                        conjugations_dic[template_name][mood.tag][tense.tag] = self.load_tense(mood, tense)
        self.conjugations = conjugations_dic

    def load_tense(self, mood, tense):
        # Manage past participle
        persons = list(tense)
        if tense.tag in ('infinitive-present', 'present-participle'):
            if persons[0].find("i") is not None:
                conjug = persons[0].find("i").text
            else:
                conjug = None
        elif tense.tag == 'imperative-present':
            pronouns = ["2s :", "1p :", "2p :"]
            conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
                    not None else None) for pers, term in zip(pronouns, persons))
        elif tense.tag == 'past-participle':
            pronouns = ["ms :", "mp :", "fs :", "fp :"]
            conjug = OrderedDict((pers, term.find("i").text if term.find("i") is
                    not None else None) for pers, term in zip(pronouns, persons))
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
                    not None else None) for pers, term in zip(pronouns, persons))
        return conjug

    def get_verb_info(self, verb):
        """

        :param verb:
        :return:
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

        :param template:
        :return:
        """
        if template not in self.conjugations.keys():
            return None
        else:
            return self.conjugations[template]

    def conjugate(self, word):
        """

        :param word:
        :return verb:
        """
        infinitive = None
        if word not in self.verbs.keys():
            if self.model is None:
                return None
            predicted = self.model.predict([word])[0]
            template = self.templates[predicted]
            index = - len(template[template.index(":") + 1:])
            root = word[:index]
            verb_info = VerbInfo(word, root, template)
            conjug_info = self.get_conjug_info(verb_info.template)
            pass
            pass
        else:
            infinitive = word
            verb_info = self.get_verb_info(infinitive)
            if verb_info is None:
                return None
            conjug_info = self.get_conjug_info(verb_info.template)
            if conjug_info is None:
                return None
        verb = Verb(verb_info, conjug_info)
        return verb

    def set_model(self, model):
        self.model = model
        return


class VerbInfo(object):
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
    __slots__ = ('name', 'verb_info', 'conjug_info')
    def __init__(self, verb_info, conjug_info):
        """

        :param verb_info:
        :param conjug_info:
        """
        self.name = verb_info.infinitive
        self.verb_info = verb_info
        self.conjug_info = conjug_info
        self.load_conjug()

    def load_conjug(self):
        """


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
