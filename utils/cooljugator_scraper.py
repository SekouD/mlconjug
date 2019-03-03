from abc import ABCMeta, abstractmethod

import re
import urllib3
from urllib.parse import quote
import certifi
import random
from collections import defaultdict
import pickle
import sys
from bs4 import BeautifulSoup

# We use gevent in order to make asynchronous http requests while downloading lyrics.
import gevent.monkey
from gevent.pool import Pool


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


def show_progress_indicator(queue):
    while True:
        gevent.sleep()
        percent = 0.0
        for i in queue:
            if i[1].successful():
                percent += 100 / len(queue)
        sys.stdout.write(
            ('=' * int(percent)) + ('' * (100 - int(percent))) + (
                "\r [ %d" % percent + "% ] "))
        sys.stdout.flush()
        if percent >= 99:
            sys.stdout.write('\n')
            sys.stdout.flush()
            break


class ConjugProvider:
    """
    This is the base class for all Lyrics Providers. If you wish to subclass this class, you must implement all
    the methods defined in this class to be compatible with the LyricsMaster API.
    Requests to fetch songs are executed asynchronously for better performance.
    Tor anonymisation is provided if tor is installed on the system and a TorController is passed at instance creation.

    :param tor_controller: TorController Object.

    """
    __metaclass__ = ABCMeta
    name = ''

    def __init__(self, tor_controller=None):
        if not self.__socket_is_patched():
            gevent.monkey.patch_socket()
        self.tor_controller = tor_controller
        if not self.tor_controller:
            retries = urllib3.Retry(35)
            user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            self.session = urllib3.PoolManager(maxsize=35,
                                               cert_reqs='CERT_REQUIRED',
                                               ca_certs=certifi.where(),
                                               headers=user_agent,
                                               retries=retries)
        else:
            self.session = self.tor_controller.get_tor_session()
        self.__tor_status__()
        self.languages = self._get_all_languages()

    def __repr__(self):
        return '{0}.{1}({2})'.format(__name__, self.__class__.__name__, self.tor_controller.__repr__())

    def __tor_status__(self):
        """
        Informs the user of the Tor status.

        """
        if not self.tor_controller:
            print('Anonymous requests disabled. The connexion will not be anonymous.')
        elif self.tor_controller and not self.tor_controller.controlport:
            print('Anonymous requests enabled. The Tor circuit will change according to the Tor network defaults.')
        else:
            print('Anonymous requests enabled. The Tor circuit will change for each album.')

    @staticmethod
    def __socket_is_patched():
        """
        Checks if the socket is patched or not.

        :return: bool.
        """
        return gevent.monkey.is_module_patched('socket')

    @abstractmethod
    def _get_all_languages(self):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Builds an url for the artist page of the lyrics provider.

        :param artist:
        :return: string or None.
        """
        pass

    @abstractmethod
    def _get_all_verbs(self, language):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Builds an url for the artist page of the lyrics provider.

        :param artist:
        :return: string or None.
        """
        pass

    @abstractmethod
    def _make_verb_url(self, artist):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Builds an url for the artist page of the lyrics provider.

        :param artist:
        :return: string or None.
        """
        pass

    @abstractmethod
    def _clean_string(self, text):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Formats the text to conform to the lyrics provider formatting.

        :param text:
        :return: string or None.
        """
        pass

    def get_page(self, url):
        """
        Fetches the supplied url and returns a request object.

        :param url: string.
        :return: urllib3.response.HTTPResponse Object or None.
        """
        if not self.__socket_is_patched():
            gevent.monkey.patch_socket()
        try:
            req = self.session.request('GET', url)
        except Exception as e:
            print(e)
            req = None
            print('Unable to download url ' + url)
        return req


class Cooljugator(ConjugProvider):
    """
    Class interfacing with https://cooljugator.com/ .
    This class is used to retrieve verbs from https://cooljugator.com/.

    """
    base_url = 'https://cooljugator.com'
    name = 'Cooljugator'

    def _get_all_languages(self):
        """
        Builds a list of urls of all languages.

        :param artist:
        :return: string or None.
        """
        raw_html = self.get_page(self.base_url).data
        index_page = BeautifulSoup(raw_html, 'lxml')
        languages = index_page.find("div",
                                    {'id': 'main-language-selection'}).contents
        languages = {lang.text.strip(): {'href': lang.attrs['href']}
                     for lang in languages if 'adjectives' not in lang.text and
                     'nouns' not in lang.text}
        return languages

    def _get_all_verbs(self, language):
        """
        Builds a list of urls for all the verbs of the language.

        :param language:
        :return: string or None.
        """
        all_verbs_url = self.base_url + self.languages[language]['href'] + '/list/all'
        response = self.get_page(all_verbs_url)
        if b'Error 404' in response._body:
            all_verbs_url = self.base_url + self.languages[language]['href'] + '/list/index'
            response = self.get_page(all_verbs_url)
        all_verbs_html = response.data
        all_verbs_page = BeautifulSoup(all_verbs_html, 'lxml')
        verbs_div = all_verbs_page.find("div",
                                        {'class': 'ui segment stacked'})
        verbs_list = verbs_div.contents[0].contents
        all_verbs = {verb.contents[0].text:
                         {'href': verb.contents[0].attrs['href']
                          } for verb in verbs_list}
        return all_verbs

    def _make_verb_url(self, verb):
        """
        Builds an url for the artist page of the lyrics provider.

        :param verb: string.
        :return: string.
        """
        url = self.base_url + quote(verb['href'])
        return url

    def get_verb_page(self, verb):
        """
        Fetches the verb's page.

        :param verb: string.
        :return: string or None.
            Album's raw html page. None if the album page was not found.
        """
        url = self._make_verb_url(verb)
        response = self.get_page(url)
        try:
            raw_html = response.data
        except AttributeError:
            return None
        verb_page = BeautifulSoup(raw_html, 'lxml')
        if not verb_page.find("section", {'id': 'conjugations'}):
            return None
        return verb_page

    def get_conjug(self, verb):
        """
        Fetches the verb conjugation info.

        :param verb: string.
        :return: dict.
            Conjugation Dict.
        """
        raw_html = self.get_verb_page(verb)
        if raw_html is None:
            conjug = None
            return conjug
        conjug_table = raw_html.find("section", {'id': 'conjugations'})
        moods = [mood_tag for mood_tag in
                  conjug_table.find_all("div",
                                        {'class':
                                            'conjugation-table collapsable'})]
        conjug = {}
        for mood in moods:
            tenses_names = mood.find_all("span", {
                'class': 'tense-title-space'})
            tenses_conjug = mood.find_all("div", {
                'class': 'meta-form'})
            pronouns = mood.find_all("div", {
                'class': 'ui ribbon label blue conjugation-pronoun'})
            for tense, conjug_table in zip(tenses_names,
                                           chunks(tenses_conjug, len(pronouns))):
                conjug[tense.text] = [(pron.text, form.text) for pron, form in
                                      zip(pronouns, conjug_table)]
                pass
        return conjug

    def _clean_string(self, text):
        """
        Cleans the supplied string and formats it to use in a url.

        :param text: string.
            Text to be cleaned.
        :return: string.
            Cleaned text.
        """
        for elmt in [('#', 'Number_'), ('[', '('), (']', ')'), ('{', '('), ('}', ')'), (' ', '_')]:
            text = text.replace(*elmt)
        return text


if __name__ == "__main__":
    conjugator = Cooljugator()
    all_languages = conjugator._get_all_languages()
    for lang in all_languages:
        if 'adjectives' in lang or 'nouns' in lang:
            continue
        conjug = {}
        test_verbs = conjugator._get_all_verbs(lang)
        print('Adding {0} download tasks for {1} verbs to queue.'.format(len(test_verbs), lang))
        # Experimental async requests
        pool = Pool(256)  # Sets the worker pool for async requests.
        results = [(verb, pool.spawn(conjugator.get_conjug, test_verbs[verb]))
                   for verb in test_verbs]
        show_progress_indicator(results)
        print('Joining pool for all {0} verbs.'.format(lang))
        pool.join()  # Gathers results from the pool
        print('Adding all {0} conjugation tables to dictionary.'.format(lang))
        for verb, conjugation in results:
            conjug[verb] = conjugation.value

        with open('cooljugator_dump-{0}.pickle'.format(lang), 'wb') as f:
            pickle.dump(conjug, f)
            print('All the {0} verbs have been saved.\n'.format(lang))
    print('OK.')
    print('All the verbs for all languages have been saved.')
    pass
