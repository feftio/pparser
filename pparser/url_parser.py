from __future__ import annotations
from pparser.utils import merge_queries
import typing as t
from urllib.parse import urlparse, urlunparse, ParseResult


class UrlParser:
    def __init__(self, url: str):
        self._parse_result: ParseResult = urlparse(url)

    def __repr__(self):
        return self._parse_result.__repr__()

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

    @property
    def path(self) -> str:
        return self._parse_result.path

    @property
    def netloc(self) -> str:
        return self._parse_result.netloc

    @property
    def scheme(self) -> str:
        return self._parse_result.scheme

    def copywith(self, **params: t.Dict[str, t.Any]) -> UrlParser:
        return UrlParser(self._parse_result._replace(**params).geturl())


if __name__ == '__main__':
    url_parser = UrlParser(
        url='https://www.youtube.com/watch?v=DKbfBSrjVHA&list=PLYZQyxV71fKP-cu4nOXuIupKmbGR7YiLC&index=68&ab_channel=7clouds')
    print(url_parser)
