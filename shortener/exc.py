"""Exceptions."""

import logging

log = logging.getLogger(__name__)


class FeedError(Exception):
    def __init__(self, msg: str, code: int):
        msg = f'[{code}] {msg}'.rstrip()
        self.code = code
        log.error(msg)
        super().__init__(msg)
