from functools import lru_cache
import logging
import urllib.error
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from bitlyshortener import Shortener as BitlyShortener
from cachetools.func import ttl_cache

from . import config
from .util.humanize import humanize_len

config.configure_logging()

log = logging.getLogger(__name__)

# TODO: Add support for Atom, e.g. https://feeds.feedburner.com/blogspot/gJZg
# TODO: Use compressed caches so as to save memory.
# TODO: Check for safety of URL.
# Refer to: https://stackoverflow.com/questions/25033741/ and https://stackoverflow.com/questions/12083578/


class FeedError(Exception):
    def __init__(self, msg: str, code: int):
        # msg = f'[{code}] {msg}'.rstrip()
        self.code = code
        log.error(msg)
        super().__init__(msg)


class Feed:
    def __init__(self) -> None:
        self._shorten_urls = BitlyShortener(tokens=config.BITLY_TOKENS,
                                            max_cache_size=config.BITLY_SHORTENER_CACHE_SIZE).shorten_urls_to_dict
        self._is_debug_logged = log.isEnabledFor(logging.DEBUG)

    @lru_cache(maxsize=config.LRU_CACHE_SIZE)
    def _output(self, text: str) -> bytes:
        try:
            xml = ElementTree.fromstring(text)
        except ElementTree.ParseError as exception:
            raise FeedError(f'Unable to parse URL content as XML: {exception}', 422)

        link_xpath = './channel/item/link'
        long_urls = (elem.text for elem in xml.iterfind(link_xpath))
        url_map = self._shorten_urls(long_urls)
        is_debug_logged = self._is_debug_logged
        for link in xml.iterfind(link_xpath):
            long_url = link.text
            short_url = url_map[long_url]
            link.text = short_url
            if is_debug_logged:
                log.debug('Replaced %s with %s.', long_url, short_url)

        log.info('Output feed has %s items.', len(xml.findall('./channel/item')))
        text_: bytes = ElementTree.tostring(xml)
        return text_

    @ttl_cache(maxsize=config.TTL_CACHE_SIZE, ttl=config.TTL_CACHE_TTL)
    def feed(self, url: str) -> bytes:
        log.debug('Reading input feed having URL %s', url)
        request = Request(url, headers={'User-Agent': config.USER_AGENT})
        try:
            response = urlopen(request, timeout=config.URL_TIMEOUT)
            text = response.read()
        except urllib.error.URLError as exception:
            raise FeedError(f'Unable to read URL: {exception}', 404)
        log.info('Input feed has size %s.', humanize_len(text))
        if response.headers[config.CYCLE_DETECTION_HEADER_KEY] == config.CYCLE_DETECTION_HEADER_VALUE:
            raise FeedError(f'Cycle detected.', 400)
        text = self._output(text)
        log.info('Output feed has size %s.', humanize_len(text))
        return text
