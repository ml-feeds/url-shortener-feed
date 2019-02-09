from __future__ import annotations
import abc
from enum import Enum
from typing import Dict, List, Optional
from xml.etree import ElementTree


class _BaseLink(metaclass=abc.ABCMeta):
    NAMESPACES: Optional[Dict[str, str]] = None

    def __init__(self, element: ElementTree.Element):
        self._element = element

    @classmethod
    def findall(cls, xml: ElementTree.Element) -> List[_BaseLink]:
        return [cls(element) for element in xml.findall(cls.XPATH, namespaces=cls.NAMESPACES)]  # type: ignore

    @property  # type: ignore
    @abc.abstractmethod
    def link(self) -> str:
        pass

    @link.setter  # type: ignore
    @abc.abstractmethod
    def link(self, link: str) -> None:
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def NAME(cls) -> str:
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def XPATH(cls) -> str:
        pass


class _BaseRSSLink(_BaseLink):
    @property
    def link(self) -> str:
        return self._element.text  # type: ignore

    @link.setter
    def link(self, link: str) -> None:
        self._element.text = link


class _LinkTypes(Enum):

    class RSS2Link(_BaseRSSLink):  # Example: http://www.infoworld.com/category/artificial-intelligence/index.rss
        NAME = 'RSS2'
        XPATH = './channel/item/link'

    class RSS1Link(_BaseRSSLink):  # Example: https://export.arxiv.org/rss/eess.IV/recent
        NAME = 'RSS1'
        NAMESPACES = {'rss': 'http://purl.org/rss/1.0/'}
        XPATH = './rss:item/rss:link'

    class AtomLink(_BaseLink):  # Example: https://feeds.feedburner.com/blogspot/gJZg
        NAME = 'Atom'
        NAMESPACES = {'atom': 'http://www.w3.org/2005/Atom'}
        XPATH = "./atom:entry/atom:link[@rel='alternate'][@href][@title]"

        @property
        def link(self) -> str:
            return self._element.attrib['href']

        @link.setter
        def link(self, link: str) -> None:
            self._element.attrib['href'] = link


LINK_TYPES = [member.value for member in _LinkTypes]
