from __future__ import annotations
import typing as t
from urllib.parse import urlparse, urlunparse, ParseResult


class UrlParser:
    def __init__(self, url: str):
        self._url: ParseResult = urlparse(url)

    @property
    def full_url(self) -> str:
        return self._url.geturl()

    @property
    def root_url(self) -> str:
        return urlunparse((self._url.scheme, self._url.netloc, *([''] * 4)))

    @property
    def url(self) -> str:
        return urlunparse((self._url.scheme, self._url.netloc, self._url.path, *([''] * 3)))

    @property
    def query(self) -> str:
        return self._url.query

    def copywith(self, **params):
        return UrlParser(self._url._replace(**params).geturl())