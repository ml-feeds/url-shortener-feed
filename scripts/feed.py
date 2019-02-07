import logging
import time

from shortener.feed import Feed

log = logging.getLogger(__name__)

if __name__ == '__main__':
    feed = Feed()
    try:
        output = feed.feed('https://us-east1-ml-feeds.cloudfunctions.net/pwc/trending')
        print(output.decode())

        # log.info('Testing cachetools cache.')
        # assert feed.feed() == output
        # log.info('Tested cachetools cache.')
    except Exception:
        time.sleep(.01)  # Delay for logs to flush.
        raise
