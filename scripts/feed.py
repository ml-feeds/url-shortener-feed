import logging
import time

from shortener.feed import Feed

log = logging.getLogger(__name__)

URL = 'https://feeds.feedburner.com/blogspot/gJZg'
# URL = 'https://us-east1-ml-feeds.cloudfunctions.net/nvidia-research-ml'

if __name__ == '__main__':
    feed = Feed()
    try:
        output = feed.feed(URL)
        print(output.decode())

        log.info('Testing cachetools cache.')
        assert feed.feed(URL) == output
        log.info('Tested cachetools cache.')
    except Exception:
        time.sleep(.01)  # Delay for logs to flush.
        raise
