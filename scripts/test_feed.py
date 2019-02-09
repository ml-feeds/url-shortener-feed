import logging
import time

from shortener.feed import Feed

log = logging.getLogger(__name__)

ATOM_URL = 'https://feeds.feedburner.com/blogspot/gJZg'
RSS_URL = 'http://www.infoworld.com/category/artificial-intelligence/index.rss'

if __name__ == '__main__':
    feed = Feed()
    url = RSS_URL
    try:
        output = feed.feed(url)
        print(output.decode())

        log.info('Testing cachetools cache.')
        assert feed.feed(url) == output
        log.info('Tested cachetools cache.')
    except Exception:
        time.sleep(.01)  # Delay for logs to flush.
        raise