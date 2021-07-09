from __future__ import annotations
import typing as t
from urllib.parse import parse_qsl, urlencode
import asyncio

__all__ = [
    'stringify_query',
    'merge_queries',
    'merge_dicts',
    'run_async'
]


def stringify_query(query: t.Union[str, t.Dict[str, t.Any]]) -> str:
    if isinstance(query, dict):
        return urlencode(query)
    elif isinstance(query, str):
        return query
    else:
        raise TypeError(
            f'Argument by {query.__class__} must be instance of "str" or "dict".')


def merge_queries(queryb: t.Union[str, t.Dict[str, t.Any]], querys: t.Union[str, t.Dict[str, t.Any]]) -> str:
    queryb, querys = stringify_query(queryb), stringify_query(querys)
    return urlencode({**dict(parse_qsl(queryb)), **dict(parse_qsl(querys))})


def merge_dicts(*dicts, expandable: bool = False):
    dicts = list(dicts)
    c = dicts.pop(0)
    for _ in range(len(dicts)):
        n = dicts.pop(0)
        for k in n.keys():
            if k in c:
                if isinstance(c[k], list):
                    c[k].extend(n[k])
                    c[k] = list(set(c[k]))
                else:
                    c[k] = n[k]
            else:
                if expandable:
                    c[k] = n[k]
    return dict(c)


def run_async(awaitable):
    return asyncio.get_event_loop().run_until_complete(awaitable)
