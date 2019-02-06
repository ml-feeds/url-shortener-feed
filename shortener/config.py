import datetime
import logging.config
import os
from pathlib import Path
from typing import List


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING)
    log = logging.getLogger(__name__)
    log.debug('Logging is configured.')


def _env_key_to_list(env_key: str) -> List[str]:
    return [s.strip() for s in os.getenv(env_key, '').strip().split(',') if s.strip()]


BITLY_SHORTENER_CACHE_SIZE = 2048
BITLY_TOKENS = _env_key_to_list('BITLY_TOKENS')
CACHE_SIZE = 128
CACHE_TTL = datetime.timedelta(minutes=58).total_seconds()
ON_SERVERLESS = bool(os.getenv('GCLOUD_PROJECT'))
PACKAGE_NAME = Path(__file__).parent.stem
SAMPLE_FEED_URL = 'https://us-east1-ml-feeds.cloudfunctions.net/kdnuggets'
USER_AGENT = 'Mozilla/5.0'
USF_TOKENS = _env_key_to_list('USF_TOKENS')

LOGGING = {  # Ref: https://docs.python.org/3/howto/logging.html#configuring-logging
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '[%(relativeCreated)i] %(name)s:%(lineno)d:%(funcName)s:%(levelname)s: %(message)s',
        },
        'serverless': {
            'format': '%(thread)x:%(name)s:%(lineno)d:%(funcName)s:%(levelname)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'serverless' if ON_SERVERLESS else 'detailed',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        PACKAGE_NAME: {
            'level': 'INFO' if ON_SERVERLESS else 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'bitlyshortener': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
         },
    },
}

