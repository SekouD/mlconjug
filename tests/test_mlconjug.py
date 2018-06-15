#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlconjug` package."""

import pytest
import os

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from click.testing import CliRunner

from collections import OrderedDict

from mlconjug import mlconjug, PyVerbiste
from mlconjug import cli


LANGUAGES = ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro')

VERBS = {'default': PyVerbiste.Verb,
         'fr': PyVerbiste.VerbFr,
         'en': PyVerbiste.VerbEn,
         'es': PyVerbiste.VerbEs,
         'it': PyVerbiste.VerbIt,
         'pt': PyVerbiste.VerbPt,
         'ro': PyVerbiste.VerbRo}

TEST_VERBS = {'fr': ('manger', 'man:ger'),
         'en': ('bring', 'br:ing'),
         'es': ('gallofar', 'cort:ar'),
         'it': ('lavare', 'lav:are'),
         'pt': ('anunciar', 'compr:ar'),
         'ro': ('cambra', 'dans:a')}

class TestPyVerbiste:
    verbiste = PyVerbiste.Verbiste(language='fr')
    def test_init_verbiste(self):
        assert len(self.verbiste.templates) == len(self.verbiste.conjugations) == 149
        assert self.verbiste.templates[0] == ':aller'
        assert self.verbiste.templates[-1] == 'écri:re'
        assert isinstance(self.verbiste.conjugations[':aller'], OrderedDict)
        assert len(self.verbiste.verbs) == 7015
        assert self.verbiste.verbs['abaisser'] == {'template': 'aim:er', 'root': 'abaiss'}

    def test_get_verb_info(self):
        verb_info = self.verbiste.get_verb_info('aller')
        assert verb_info == PyVerbiste.VerbInfo('aller', '', ':aller')
        assert self.verbiste.get_verb_info('cacater') is None

    def test_get_conjug_info(self):
        conjug_info = self.verbiste.get_conjug_info(':aller')
        assert conjug_info == self.verbiste.conjugations[':aller']
        assert self.verbiste.get_conjug_info(':cacater') is None

class TestVerb:
    def test_verbinfo(self):
        for lang in LANGUAGES:
            verbiste = PyVerbiste.Verbiste(language=lang)
            test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
            test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
            test_verb = VERBS[verbiste.language](test_verb_info, test_conjug_info)
            assert isinstance(test_verb, VERBS[verbiste.language])
            assert isinstance(test_verb.conjug_info, OrderedDict)


class TestEndingCountVectorizer:
    ngrange = (2, 7)
    vectorizer = mlconjug.EndingCountVectorizer(analyzer="char", binary=True, ngram_range=ngrange)
    def test_char_ngrams(self):
        ngrams = self.vectorizer._char_ngrams('aller')
        assert 'ller' in ngrams


class TestConjugator:
    conjugator = mlconjug.Conjugator()
    def test_conjugate(self):
        test_verb = self.conjugator.conjugate('aller')
        assert isinstance(test_verb, PyVerbiste.Verb)
        assert test_verb.verb_info == PyVerbiste.VerbInfo('aller', '', ':aller')
        test_verb = self.conjugator.conjugate('cacater')
        assert isinstance(test_verb, PyVerbiste.Verb)

    def test_set_model(self):
        self.conjugator.set_model(mlconjug.Model())
        assert isinstance(self.conjugator.model, mlconjug.Model)


class TestDataSet:
    data_set = mlconjug.DataSet(mlconjug.Verbiste())
    def test_construct_dict_conjug(self):
        self.data_set.construct_dict_conjug()
        assert 'aller' in self.data_set.dict_conjug[':aller']

    def test_split_data(self):
        self.data_set.split_data()
        assert self.data_set.test_input is not None
        assert self.data_set.train_input is not None
        assert self.data_set.test_labels is not None
        assert self.data_set.train_labels is not None


class TestModel:
    vectorizer = mlconjug.EndingCountVectorizer(analyzer="char", binary=True,
                                                ngram_range=(2, 7))
    # Feature reduction
    feature_reductor = mlconjug.SelectFromModel(
        mlconjug.LinearSVC(penalty="l1", max_iter=3000, dual=False, verbose=2))
    # Prediction Classifier
    classifier = mlconjug.SGDClassifier(loss="log", penalty='elasticnet',
                                        alpha=1e-5, random_state=42)
    # Initialize Model
    model = mlconjug.Model(vectorizer, feature_reductor, classifier)
    dataset = mlconjug.DataSet(mlconjug.Verbiste())
    dataset.construct_dict_conjug()
    dataset.split_data(proportion=0.9)

    def test_train(self):
        self.model.train(self.dataset.test_input, self.dataset.test_labels)
        assert isinstance(self.model, mlconjug.Model)

    def test_predict(self):
        result = self.model.predict(['aimer',])
        assert self.dataset.templates[result[0]] == 'aim:er'



def test_command_line_interface():
    """Test the CLI."""
    verb = 'aller'
    runner = CliRunner()
    result = runner.invoke(cli.main, [verb])
    assert result.exit_code == 0
    assert 'allassions' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Console script for mlconjug.' in help_result.output
