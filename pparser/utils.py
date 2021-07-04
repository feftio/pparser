from __future__ import annotations
import typing as t
from urllib.parse import parse_qsl, urlencode

def stringify_query(query: t.Union[str, t.Dict[str, t.Any]]) -> str:
    if isinstance(query, dict):
        return urlencode(query)
    elif isinstance(query, str):
        return query
    else:
        raise TypeError(f'Argument by {query.__class__} must be instance of "str" or "dict".')


def merge_queries(queryb: t.Union[str, t.Dict[str, t.Any]], querys: t.Union[str, t.Dict[str, t.Any]]) -> str:
    queryb, querys = stringify_query(queryb), stringify_query(querys)
    return urlencode({**dict(parse_qsl(queryb)), **dict(parse_qsl(querys))})


if __name__ == '__main__':
    assert merge_queries('a=1&b=2&c=3', {'c': 4, 'd': '5'}) == 'a=1&b=2&c=4&d=5'
