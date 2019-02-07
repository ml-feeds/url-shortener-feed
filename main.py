import logging
from secrets import compare_digest
from typing import Dict, Tuple, Union

import flask

from shortener import config
from shortener.feed import Feed, FeedError
from shortener.util.resource import MemUse

log = logging.getLogger(__name__)
feed = Feed()
Response = Tuple[Union[bytes, str], int, Dict[str, str]]
mem = MemUse()


def _is_authorized(token: str) -> bool:
    return any(compare_digest(token, approved_token) for approved_token in config.USF_TOKENS)


def _is_sampling(token: str, url: str) -> bool:
    return (token == 'sample') and (url == config.SAMPLE_FEED_URL)


def _response(msg: Union[bytes, str], code: int, ip: str) -> Response:
    mem.log_use()
    if code >= 400:
        log.error('Error %s while handling request from %s: %s', code, ip, msg)
        return f'ERROR: {msg}', code, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        return msg, code, {'Content-Type': 'text/xml; charset=utf-8',
                           config.CYCLE_DETECTION_HEADER_KEY: config.CYCLE_DETECTION_HEADER_VALUE}


def serve(request: flask.Request) -> Response:
    hget = request.headers.get
    ip = hget('X-Appengine-User-Ip')
    token, url = request.args.get('token'), request.args.get('url')
    log.info('Received request using token starting with %s from %s from %s, %s, %s for URL %s.',
             str(token)[:4], ip, hget('X-Appengine-City'), hget('X-Appengine-Region'), hget('X-Appengine-Country'), url)

    if all([token, url]) and (_is_authorized(token) or _is_sampling(token, url)):
        try:
            output = feed.feed(url)
        except FeedError as exc:
            return _response(str(exc), exc.code, ip)
        return _response(output, 200, ip)
    else:
        msg = 'Invalid request. Specify valid values for query parameters "token" and "url". Use of this service is ' \
              'restricted to approved users.'
        return _response(msg, 401, ip)
