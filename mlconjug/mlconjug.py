# -*- coding: utf-8 -*-

"""Main module."""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


import random
from collections import defaultdict, OrderedDict


class EndingCountVectorizer(CountVectorizer):
    """Custom Vectorizer optimized for extracting verbs features"""
    def _char_ngrams(self, text_document):
        """Tokenize text_document into a sequence of ending character n-grams"""
        text_document = self._white_spaces.sub(" ", text_document)
        text_len = len(text_document)
        ngrams = []
        min_n, max_n = self.ngram_range
        for n in range(min_n, min(max_n + 1, text_len + 1)):
            ngram = text_document[-n:]
            ngrams.append(ngram)
        return ngrams



class DataSet:
    """

    :param VerbisteObj:

    :return:
    """
    def __init__(self, VerbisteObj):
        self.verbiste = VerbisteObj
        self.verbes = self.verbiste.verbes.keys()
        self.templates = sorted(self.verbiste.conjugaisons.keys())
        self.liste_verbes = []
        self.liste_templates = []
        self.dict_conjug = []
        self.train_input = []
        self.train_labels = []
        self.test_input = []
        self.test_labels = []

    def construct_dict_conjug(self):
        """

        :return:
        """
        conjug = defaultdict(list)
        for verbe, info_verbe in self.verbiste.verbes.items():
            self.liste_verbes.append(verbe)
            self.liste_templates.append(
                self.templates.index(info_verbe["template"]))
            conjug[info_verbe["template"]].append(verbe)
        self.dict_conjug = conjug
        return

    def split_data(self, threshold=8, proportion=0.5):
        """

        :param threshold:
        :param proportion:
        :return:
        """
        if proportion <= 0 or proportion >= 1:
            raise ValueError('The split proportion must be between 0 and 1')
        self.min_threshold = threshold
        self.split_proportion = proportion
        train_set = []
        test_set = []
        for template, lverbes in self.dict_conjug.items():
            if len(lverbes) <= threshold:
                for verbe in lverbes:
                    train_set.append((verbe, template))
            else:
                index = round(len(lverbes) * proportion)
                for verbe in lverbes[:index]:
                    train_set.append((verbe, template))
                for verbe in lverbes[index:]:
                    test_set.append((verbe, template))
        random.shuffle(train_set)
        random.shuffle(test_set)
        self.train_input = [elmt[0] for elmt in train_set]
        self.train_labels = [self.templates.index(elmt[1]) for elmt in
                             train_set]
        self.test_input = [elmt[0] for elmt in test_set]
        self.test_labels = [self.templates.index(elmt[1]) for elmt in test_set]
        return


class Model(object):
    """

    :param vectorizer:
    :param feature_selector:
    :param classifier:
    """
    def __init__(self, vectorizer, feature_selector, classifier):
        self.model = Pipeline([('vectorizer', vectorizer),
                               ('feature_selector', feature_selector),
                               ('classifier', classifier)])

    def train(self, samples, labels):
        """

        :param samples:
        :param labels:
        """
        self.model = self.model.fit(samples, labels)

    def predict(self, verbs):
        """

        :param verbs:
        """
        prediction = self.model.predict(verbs)
