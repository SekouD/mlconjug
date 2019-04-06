#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlconjug` package."""

import pytest
import os

from sklearn.exceptions import ConvergenceWarning
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

from functools import partial

from click.testing import CliRunner

from collections import OrderedDict

from mlconjug import Conjugator, DataSet, Model, extract_verb_features,\
    LinearSVC, SGDClassifier,SelectFromModel, CountVectorizer

from mlconjug import Verbiste, VerbInfo, Verb, VerbEn,\
    VerbEs, VerbFr, VerbIt, VerbPt, VerbRo, ConjugManager

from mlconjug import cli


LANGUAGES = ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro')

VERBS = {'default': Verb,
         'fr': VerbFr,
         'en': VerbEn,
         'es': VerbEs,
         'it': VerbIt,
         'pt': VerbPt,
         'ro': VerbRo}

TEST_VERBS = {'fr': ('manger', 'man:ger'),
         'en': ('bring', 'br:ing'),
         'es': ('gallofar', 'cort:ar'),
         'it': ('lavare', 'lav:are'),
         'pt': ('anunciar', 'compr:ar'),
         'ro': ('cambra', 'dans:a')}

class TestPyVerbiste:
    verbiste = Verbiste(language='fr')
    verbiste_en = Verbiste(language='en')
    def test_init_verbiste(self):
        assert len(self.verbiste.templates) == len(self.verbiste.conjugations) == 149
        assert self.verbiste.templates[0] == ':aller'
        assert self.verbiste.templates[-1] == 'écri:re'
        assert isinstance(self.verbiste.conjugations[':aller'], OrderedDict)
        assert len(self.verbiste.verbs) == 7015
        assert self.verbiste.verbs['abaisser'] == {'template': 'aim:er', 'root': 'abaiss'}

    def test_repr(self):
        assert self.verbiste.__repr__() == 'mlconjug.PyVerbiste.Verbiste(language=fr)'

    def test_unsupported_language(self):
        with pytest.raises(ValueError) as excinfo:
            Verbiste(language='de')
        # assert 'Unsupported language.' in str(excinfo.value)

    def test_get_verb_info(self):
        verb_info = self.verbiste.get_verb_info('aller')
        assert verb_info == VerbInfo('aller', 'aller', ':aller')
        assert self.verbiste.get_verb_info('cacater') is None
        assert verb_info.__repr__() == 'mlconjug.PyVerbiste.VerbInfo(aller, aller, :aller)'

    def test_get_conjug_info(self):
        conjug_info = self.verbiste.get_conjug_info(':aller')
        conjug_info2 = self.verbiste.get_conjug_info('man:ger')
        assert conjug_info != conjug_info2
        assert conjug_info == self.verbiste.conjugations[':aller']
        assert self.verbiste.get_conjug_info(':cacater') is None

    def test_is_valid_verb(self):
        assert self.verbiste.is_valid_verb('manger')
        assert not self.verbiste.is_valid_verb('banane')
        assert self.verbiste_en.is_valid_verb('bring')

class TestVerb:
    def test_verbinfo(self):
        for lang in LANGUAGES:
            verbiste = Verbiste(language=lang)
            test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
            test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
            test_verb = VERBS[verbiste.language](test_verb_info, test_conjug_info)
            assert isinstance(test_verb, VERBS[verbiste.language])
            assert isinstance(test_verb.conjug_info, OrderedDict)

    def test_default_verb(self):
        verbiste = Verbiste(language='default')
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = Verb(test_verb_info, test_conjug_info)
        assert isinstance(test_verb, Verb)
        assert isinstance(test_verb.conjug_info, OrderedDict)

    def test_repr(self):
        verbiste = Verbiste(language='fr')
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = VerbFr(test_verb_info, test_conjug_info)
        assert test_verb.__repr__() == 'mlconjug.PyVerbiste.VerbFr(manger)'


class TestEndingCountVectorizer:
    ngrange = (2, 7)
    custom_vectorizer = partial(extract_verb_features, lang='fr', ngram_range=ngrange)
    vectorizer = CountVectorizer(analyzer=custom_vectorizer, binary=True, ngram_range=ngrange)
    def test_char_ngrams(self):
        ngrams = self.vectorizer._char_ngrams('aller')
        assert 'ller' in ngrams


class TestConjugator:
    conjugator = Conjugator()
    def test_repr(self):
        assert self.conjugator.__repr__() == 'mlconjug.mlconjug.Conjugator(language=fr)'

    def test_conjugate(self):
        test_verb = self.conjugator.conjugate('aller')
        assert isinstance(test_verb, Verb)
        assert test_verb.verb_info == VerbInfo('aller', '', ':aller')
        test_verb = self.conjugator.conjugate('cacater')
        assert isinstance(test_verb, Verb)
        with pytest.raises(ValueError) as excinfo:
            self.conjugator.conjugate('blablah')
        # assert 'The supplied word: blablah is not a valid verb in French.' in str(excinfo.value)

    def test_set_model(self):
        self.conjugator.set_model(Model())
        assert isinstance(self.conjugator.model, Model)


class TestDataSet:
    conjug_manager = ConjugManager()
    data_set = DataSet(conjug_manager.verbs)
    def test_repr(self):
        assert self.data_set.__repr__() == 'mlconjug.mlconjug.DataSet()'

    def test_construct_dict_conjug(self):
        self.data_set.construct_dict_conjug()
        assert 'aller' in self.data_set.dict_conjug[':aller']

    def test_split_data(self):
        self.data_set.split_data()
        assert self.data_set.test_input is not None
        assert self.data_set.train_input is not None
        assert self.data_set.test_labels is not None
        assert self.data_set.train_labels is not None
        with pytest.raises(ValueError) as excinfo:
            self.data_set.split_data(proportion=2)
        # assert 'The split proportion must be between 0 and 1' in str(excinfo.value)


class TestModel:
    extract_verb_features = extract_verb_features
    vectorizer = CountVectorizer(analyzer=partial(extract_verb_features, lang='fr', ngram_range=(2,7)), binary=True, ngram_range=(2, 7))
    # Feature reduction
    feature_reductor = SelectFromModel(
        LinearSVC(penalty="l1", max_iter=3000, dual=False, verbose=2))
    # Prediction Classifier
    classifier = SGDClassifier(loss="log", penalty='elasticnet', alpha=1e-5, random_state=42)
    # Initialize Model
    model = Model(vectorizer, feature_reductor, classifier)
    dataset = DataSet(Verbiste().verbs)
    dataset.construct_dict_conjug()
    dataset.split_data(proportion=0.9)

    def test_repr(self):
        assert self.model.__repr__() == 'mlconjug.mlconjug.Model(classifier, feature_selector, vectorizer)'

    def test_train(self):
        self.model.train(self.dataset.test_input, self.dataset.test_labels)
        assert isinstance(self.model, Model)

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
    # assert 'Console script for mlconjug.' in help_result.output
