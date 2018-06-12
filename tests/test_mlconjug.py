#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlconjug` package."""

import pytest
import os

from click.testing import CliRunner

from collections import OrderedDict

from mlconjug import mlconjug, PyVerbiste
from mlconjug import cli


conjug_aller = OrderedDict([
    ('infinitive', OrderedDict([('infinitive-present', 'aller')])),
    ('indicative', OrderedDict([
        ('present', OrderedDict([('1s', 'vais'), ('2s', 'vas'), ('3s', 'va'),
                                 ('1p', 'allons'), ('2p', 'allez'), ('3p', 'vont')])),
        ('imperfect', OrderedDict([('1s', 'allais'), ('2s', 'allais'), ('3s', 'allait'),
                                   ('1p', 'allions'), ('2p', 'alliez'), ('3p', 'allaient')])),
        ('future', OrderedDict([('1s', 'irai'), ('2s', 'iras'), ('3s', 'ira'),
                                ('1p', 'irons'), ('2p', 'irez'), ('3p', 'iront')])),
        ('simple-past', OrderedDict([('1s', 'allai'), ('2s', 'allas'), ('3s', 'alla'),
                                     ('1p', 'allâmes'), ('2p', 'allâtes'), ('3p', 'allèrent')]))])),
    ('conditional', OrderedDict([
        ('present', OrderedDict([('1s', 'irais'), ('2s', 'irais'), ('3s', 'irait'),
                                 ('1p', 'irions'), ('2p', 'iriez'), ('3p', 'iraient')]))])),
    ('subjunctive', OrderedDict([
        ('present', OrderedDict([('1s', 'aille'), ('2s', 'ailles'), ('3s', 'aille'),
                                 ('1p', 'allions'), ('2p', 'alliez'), ('3p', 'aillent')])),
        ('imperfect', OrderedDict([('1s', 'allasse'), ('2s', 'allasses'), ('3s', 'allât'),
                                   ('1p', 'allassions'), ('2p', 'allassiez'), ('3p', 'allassent')]))])),
    ('imperative', OrderedDict([
        ('imperative-present', OrderedDict([('2s :', 'va'), ('1p :', 'allons'), ('2p :', 'allez')]))])),
    ('participle', OrderedDict([
        ('present-participle', 'allant'),
        ('past-participle', OrderedDict([('ms :', 'allé'), ('mp :', 'allés'),
                                         ('fs :', 'allée'), ('fp :', 'allées')]))]))])

class TestPyVerbiste:
    verbiste = PyVerbiste.Verbiste(language='fr')
    def test_init_verbiste(self):
        assert len(self.verbiste.templates) == len(self.verbiste.conjugations) == 149
        assert self.verbiste.templates[0] == ':aller'
        assert self.verbiste.templates[-1] == 'écri:re'
        assert self.verbiste.conjugations[':aller'] == conjug_aller
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
    verbiste = PyVerbiste.Verbiste(language='fr')
    def test_verbinfo(self):
        test_verb_info = self.verbiste.get_verb_info('aller')
        test_conjug_info = self.verbiste.get_conjug_info(':aller')
        test_verb = PyVerbiste.Verb(test_verb_info, test_conjug_info)
        assert test_verb.conjug_info == conjug_aller


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
        assert test_verb.conjug_info == conjug_aller
        assert test_verb.verb_info == PyVerbiste.VerbInfo('aller', '', ':aller')

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
