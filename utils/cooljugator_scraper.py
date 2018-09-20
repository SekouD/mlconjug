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
# It is also used to patch the socket module to use SOCKS5 instead to interface with the Tor controller.
import gevent.monkey
from gevent.pool import Pool

# from utils.utils import TorController


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

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
            user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            self.session = urllib3.PoolManager(maxsize=10, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(),
                                               headers=user_agent)
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

    def get_conjug(self, language, verb):
        """
        This is the main method of this class.
        Connects to the Lyrics Provider and downloads lyrics for all the albums of the supplied artist and songs.
        Returns a Discography Object or None if the artist was not found on the Lyrics Provider.

        :param artist: string
            Artist name.
        :return: models.Discography object or None.
        """

        raw_html = self.get_artist_page(artist)
        if not raw_html:
            print('{0} was not found on {1}'.format(artist, self.name))
            return None
        albums = self.get_albums(raw_html)
        if album:
            # If user supplied a specific album
            albums = [elmt for elmt in albums if album.lower() in self.get_album_infos(elmt)[0].lower()]
        album_objects = []
        for elmt in albums:
            try:
                album_title, release_date = self.get_album_infos(elmt)
            except ValueError as e:
                pass
                print('Error {0} while downloading {1}'.format(e, album_title))
                continue
            song_links = self.get_songs(elmt)
            if song:
                # If user supplied a specific song
                song_links = [link for link in song_links if song.lower() in link.text.lower()]
            if self.tor_controller and self.tor_controller.controlport:
                # Renew Tor circuit before starting downloads.
                self.tor_controller.renew_tor_circuit()
                self.session = self.tor_controller.get_tor_session()
            print('Downloading {0}'.format(album_title))
            pool = Pool(25)  # Sets the worker pool for async requests. 25 is a nice value to not annoy site owners ;)
            results = [pool.spawn(self.create_song, *(link, artist, album_title)) for link in song_links]
            pool.join()  # Gathers results from the pool
            songs = [song.value for song in results]
            album_obj = Album(album_title, artist, songs, release_date)
            album_objects.append(album_obj)
            print('{0} succesfully downloaded'.format(album_title))
        discography = Discography(artist, album_objects)
        return discography

    def get_verb_page(self, verb):
        """
        Fetches the web page for the supplied artist.

        :param artist: string.
            Artist name.
        :return: string or None.
            Artist's raw html page. None if the artist page was not found.
        """
        artist = self._clean_string(artist)
        url = self._make_artist_url(artist)
        if not url:
            return None
        raw_html = self.get_page(url).data
        artist_page = BeautifulSoup(raw_html, 'lxml')
        if not self._has_artist(artist_page):
            return None
        return raw_html

    @abstractmethod
    def get_verb_infos(self, tag):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Extracts the Album informations from the tag

        :param tag: BeautifulSoup object.
        :return: tuple(string, string).
            Album title and release date.
        """
        pass


class Cooljugator(ConjugProvider):
    """
    Class interfacing with https://cooljugator.com/ .
    This class is used to retrieve verbs from https://cooljugator.com/.

    """
    base_url = 'https://cooljugator.com'
    name = 'Cooljugator'

    def _get_all_languages(self):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.
    a                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               a
        Builds an url for the artist page of the lyrics provider.

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
        Must be implemented by children classes conforming to the LyricsMaster API.

        Builds an url for the artist page of the lyrics provider.

        :param artist:
        :return: string or None.
        """
        all_verbs_url = self.base_url + self.languages[language]['href'] + \
                    '/list/all'
        response = self.get_page(all_verbs_url)
        if response.status == 404:
            all_verbs_url = self.base_url + self.languages[language]['href'] + \
                            '/list/index'
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

        :param artist:
        :return: string.
        """
        url = self.base_url + quote(verb['href'])
        return url

    def get_verb_page(self, verb):
        """
        Fetches the album page for the supplied artist and album.

        :param artist: string.
            Artist name.
        :param album: string.
            Album title.
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
        Fetches the albums section in the supplied html page.

        :param raw_artist_page: Artist's raw html page.
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

    def get_verb_infos(self, tag):
        """
        Extracts the Album informations from the tag

        :param tag: BeautifulSoup object.
        :return: tuple(string, string).
            Album title and release date.
        """
        try:
            i = tag.text.index(' (')
            release_date = re.findall(r'\(([^()]+)\)', tag.text)[0]
        except ValueError:
            i = -1
            release_date = 'Unknown'
        album_title = tag.text[:i]

        return album_title, release_date

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
    # lang = random.choice(list(all_languages.keys()))
    conjug = defaultdict(dict)
    # with open('C:/Users/SekouD/Documents/Projets_Python/mlconjug/utils'
    #           '/raw_data/cooljugator_dump.pickle', 'rb') as f:
    #     conjug = pickle.load(f)
    #     TODO: Skip saved languagesSekouD <sekoud.pythonail.com>
    # 00150f22c5a6e5f9c928716
    for lang in all_languages:
        # if lang == 'Afrikaans':
        #     continue
        test_verbs = conjugator._get_all_verbs(lang)
        if len(test_verbs) == len(conjug[lang]):
            print('Skipping {0} verbs as they have already been downloaded'.format(lang))
            continue
        # test_verbs = conjugator._get_all_verbs(' Icelandic')
        print('Adding download tasks for {0} verbs to queue.'.format(lang))
        # verbs_list = test_verbs.keys()
        # Experimental async requests
        pool = Pool(25)  # Sets the worker pool for async requests.
        # 25 is a nice value to not annoy site owners ;)
        results = [(verb, pool.spawn(conjugator.get_conjug, test_verbs[verb]))
                   for verb in test_verbs]
        print('Joining pool for all {0} verbs.'.format(lang))
        pool.join()  # Gathers results from the pool
        print('Adding all {0} conjugation tables to dictionary.'.format(lang))
        for verb, conjugation in results:
            conjug[lang][verb] = conjugation.value
        pass
        # last_verbs = []
        # for verb in test_verbs:
        #     if verb not in conjug[lang]:
        #         conjug[lang][verb] = conjugator.get_conjug(test_verbs[verb])
        #         # print('The {0} verb {1} has been succesfully retrieved.'.format(
        #         #     lang, verb))
        #         last_verbs.append(verb)
        #         if len(last_verbs) % 50 == 0:
        #             print('The last 50 {0} verbs have been downloaded.'.format(
        #                 lang))
        #     else:
        #         pass
        #     if len(last_verbs) == 500:
        #         with open('C:/Users/SekouD/Documents/Projets_Python/mlconjug/'
        #                   'utils/raw_data/cooljugator_dump.pickle', 'wb') as f:
        #             pickle.dump(conjug, f)
        #             last_verbs_string = ', '.join(last_verbs)
        #             print('The {0} verbs {1} have been saved.\n'.format(
        #                 lang, last_verbs_string))
        #             print('{1} out of {2} {0} verbs have been saved so far.\n'
        #                   ''.format(lang,
        #                             str(len(conjug[lang])),
        #                             str(len(test_verbs))))
        #             last_verbs = []
        #     pass
        with open('C:/Users/SekouD/Documents/Projets_Python/mlconjug/utils'
                  '/raw_data/cooljugator_dump.pickle', 'wb') as f:
            pickle.dump(conjug, f)
            print('All the {0} verbs have been saved.\n'.format(lang))
    print('OK.')
    with open('C:/Users/SekouD/Documents/Projets_Python/mlconjug/utils'
              '/raw_data/cooljugator_dump.pickle', 'wb') as f:
        pickle.dump(conjug, f)
    print('All the verbs for all languages have been saved.')
    pass
