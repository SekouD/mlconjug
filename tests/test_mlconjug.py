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
    directory = os.getcwd()
    #directory = os.path.dirname(os.getcwd())
    verbs_path = os.path.join(directory, 'mlconjug', 'data', 'verbiste', 'verbs-fr.xml')
    conjugations_path = os.path.join(directory, 'mlconjug', 'data', 'verbiste', 'conjugation-fr.xml')
    verbiste = PyVerbiste.Verbiste(verbs_path, conjugations_path)
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



def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'mlconjug.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
