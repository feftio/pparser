from __future__ import annotations
import typing as t
from urllib.parse import parse_qsl, urlencode
from collections import defaultdict
import asyncio


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


def merge_options(*options: t.Dict[t.Any, t.Any]) -> t.Dict[t.Any, t.Aby]:
    options = list(options)
    sc = defaultdict(lambda *args: args, options.pop(0))
    for _ in range(len(options)):
        sn = options.pop(0)
        for k, v in sn.items():
            if isinstance(sc[k], list):
                sc[k].extend(v)
                sc[k] = list(set(sc[k]))
            else:
                sc[k] = v
    return dict(sc)


def run_async(awaitable):
    return asyncio.get_event_loop().run_until_complete(awaitable)
