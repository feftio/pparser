from __future__ import annotations
import typing as t
from urllib.parse import urlparse, urlunparse, ParseResult


class UrlParser:
    def __init__(self, url: str):
        self._parse_result: ParseResult = urlparse(url)

    @property
    def full_url(self) -> str:
        return self._parse_result.geturl()

    @property
    def root_url(self) -> str:
        return urlunparse((self._parse_result.scheme, self._parse_result.netloc, *([''] * 4)))

    @property
    def url(self) -> str:
        return urlunparse((self._parse_result.scheme, self._parse_result.netloc, self._parse_result.path, *([''] * 3)))

    @property
    def query(self) -> str:
        return self._parse_result.query

    def copywith(self, **params: t.Dict[str, t.Any]):
        return UrlParser(self._parse_result._replace(**params).geturl())
