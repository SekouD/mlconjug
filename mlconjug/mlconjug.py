# -*- coding: utf-8 -*-

"""Main module."""

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_recall_fscore_support


import random
from collections import defaultdict, OrderedDict


class EndingCountVectorizer(CountVectorizer):
    """
    Custom Vectorizer optimized for extracting verbs features.
    The Vectorizer subclasses sklearn.feature_extraction.text.CountVectorizer
    As in Romance languages verbs are inflected by adding a morphological suffix,
    the vectorizer extracts verb endings and produces a vector representation of the verb with binary features.
    The features are the verb ending ngrams. (ngram_range is set at class initialization).

    """
    def _char_ngrams(self, verb):
        """
        Parses a verb and returns the ending ngrams.

        :param verb: string.
            Verb to vectorize.
        :return: list.
            Final ngrams of the verb.
        """
        verb = self._white_spaces.sub(" ", verb)
        verb_len = len(verb)
        ngrams = []
        min_n, max_n = self.ngram_range
        for n in range(min_n, min(max_n + 1, verb_len + 1)):
            ngram = verb[-n:]
            ngrams.append(ngram)
        return ngrams



class DataSet:
    """
    This class holds and manages the data set.
    Defines helper functions for managing Machine Learning Tasks.


    :param VerbisteObj:

    """
    def __init__(self, VerbisteObj):
        self.verbiste = VerbisteObj
        self.verbes = self.verbiste.verbs.keys()
        self.templates = sorted(self.verbiste.conjugations.keys())
        self.liste_verbes = []
        self.liste_templates = []
        self.dict_conjug = []
        self.train_input = []
        self.train_labels = []
        self.test_input = []
        self.test_labels = []

    def construct_dict_conjug(self):
        """
        Populates the dictionary containing the conjugation templates.

        :return:
        """
        conjug = defaultdict(list)
        for verbe, info_verbe in self.verbiste.verbs.items():
            self.liste_verbes.append(verbe)
            self.liste_templates.append(
                self.templates.index(info_verbe["template"]))
            conjug[info_verbe["template"]].append(verbe)
        self.dict_conjug = conjug
        return

    def split_data(self, threshold=8, proportion=0.5):
        """
        Splits the data into a training and a testing set.

        :param threshold: int.
            Minimum size of conjugation class to be split.
        :param proportion: float.
            Proportion of samples in the training set. Must be between 0 and 1.
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
    This class manages the scikit-learn model.
    The Pipeline includes a feature vectorizer, a feature selector and a classifier.
    If any of the vectorizer, feature selector or classifier is not supplied at instance declaration,
    the __init__ method will provide good default value that gets more than 98% prediction accuracy.

    :param vectorizer: scikit-learn Vectorizer.
    :param feature_selector: scikit-learn Classifier with a fit_transform() method
    :param classifier: scikit-learn Classifier with a predict() method
    """
    def __init__(self, vectorizer=None, feature_selector=None, classifier=None):
        if not vectorizer:
            vectorizer = EndingCountVectorizer(analyzer="char", binary=True, ngram_range=(2, 7))
        if not feature_selector:
            feature_selector = SelectFromModel(LinearSVC(penalty='l1', max_iter=3000, dual=False, verbose=2))
        if not classifier:
            classifier = SGDClassifier(loss='log', penalty='elasticnet', alpha=1e-5, random_state=42)
        self.model = Pipeline([('vectorizer', vectorizer),
                               ('feature_selector', feature_selector),
                               ('classifier', classifier)])

    def train(self, samples, labels):
        """
        Trains the model on the supplied samples and labels.

        :param samples: list.
            List of verbs.
        :param labels: list.
            List of verb templates.
        """
        self.model = self.model.fit(samples, labels)

    def predict(self, verbs):
        """
        Predicts the conjugation class of the provided list of verbs.

        :param verbs: list.
            List of verbs.
        :return: list.
            List of predicted conjugation groups.
        """
        prediction = self.model.predict(verbs)
        return prediction


if __name__ == "__main__":
    pass
