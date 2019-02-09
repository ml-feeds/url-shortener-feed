import logging
import time

from shortener.feed import Feed

log = logging.getLogger(__name__)

RSS2_URL = 'http://www.infoworld.com/category/artificial-intelligence/index.rss'
RSS1_URL = 'https://export.arxiv.org/rss/eess.IV/recent'
ATOM_URL = 'https://feeds.feedburner.com/blogspot/gJZg'

if __name__ == '__main__':
    feed = Feed()
    url = RSS2_URL
    try:
        output = feed.feed(url)
        print(output.decode())

        log.info('Testing cachetools cache.')
        assert feed.feed(url) == output
        log.info('Tested cachetools cache.')
    except Exception:
        time.sleep(.01)  # Delay for logs to flush.
        raise
