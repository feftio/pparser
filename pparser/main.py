# -*- coding: utf-8 -*-

'''
pparser.main
~~~~~~~~~~~~

This module provides a PParser object to manage 
bs4 and pyppeteer together.


'''


from __future__ import annotations
import typing as t

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from pparser.pbrowser import PBrowser
from pparser.utils import merge_queries
from pparser.url_parser import UrlParser


class PParser:

    def __init__(self, url: str, **pbrowser_options):
        self._url_parser: UrlParser = UrlParser(url)
        self._pbrowser: PBrowser = PBrowser(**pbrowser_options)

    def soup(self, options: t.Dict[str, t.Any] = {}) -> BeautifulSoup:
        '''Prepare soup by creaing a new instance :class:`bs4.BeautifulSoup`.

        Available options:
        :param query: (str|Dict[str, Any]) Change query part of the `url`.
        :param ignoreHTTPSErrors: (bool) Whether to ignore HTTPS errors. Defaults to 
            `False`.
        :param headless: (bool) Whether to run browser in headless mode. Defaults to
            `True` unless `appMode` or `devtools` options is `True`.
        :param executablePath: (str) Path to a Chromium or Chrome executable to run
            instead of default bundled Chromium.
        :param slowMo: (int|float) Slow down pyppeteer operations by the specified
            amount of milliseconds.
        :param defaultViewport: (dict) Set a consistent viewport for each page.
            Defaults to an 800x600 viewport. `None` disables default viewport.
        :param width: (int) page width in pixels. Defaults to `1920`.
        :param height: (int) page height in pixels. Defaults to `1080`.
        :param deviceScaleFactor: (int|float) Specify device scale factor (can be
            thought as dpr). Defaults to `1`.
        :param isMobile: (bool) Whether the `meta viewport` tag is taken into
            account. Defaults to `False`.
        :param hasTouch: (bool) Specify if viewport supports touch events.
            Defaults to `False`.
        :param isLandscape: (bool) Specify if viewport is in landscape mode.
            Defaults to `False`.
        :param args: (List[str]) Additional arguments (flags) to pass to the browser
            process.
        :param ignoreDefaultArgs: (bool or List[str]) If `True`, do not use
            :func:`~pyppeteer.defaultArgs`. If list is given, then filter 
            out givendefault arguments. Dangerous option; use with care.
            Defaults to `False`.
        :param handleSIGINT: (bool) Close the browser process on Ctrl+C. Defaults to
            `True`.
        :param handleSIGTERM: (bool) Close the browser process on SIGTERM. Defaults
            to `True`.
        :param handleSIGHUP: (bool) Close the browser process on SIGHUP. Defaults to
            `True`.
        :param dumpio: (bool) Whether to pipe the browser process stdout and stderr
            into `process.stdout` and `process.stderr`. Defaults to `False`.
        :param userDataDir: (str) Path to a user data directory.
        :param env: (dict) Specify environment variables that will be visible to the
            browser. Defaults to same as python process.
        :param devtools: (bool) Whether to auto-open a DevTools panel for each tab.
            If this option is ``True``, the ``headless`` option will be set ``False``.
        :param logLevel: (int|str) Log level to print logs. Defaults to same as the
            root logger.
        :param autoClose: (bool) Automatically close browser process when script
            completed. Defaults to `True`.
        :param loop: (asyncio.AbstractEventLoop) Event loop (**experimental**).
        :param appMode: (bool) Deprecated.
        :return: Instance of :class:`bs4.BeatifulSoup` class. 
        :rtype: :class:`bs4.BeatifulSoup`.
        '''
        _url_parser = self._url_parser.copywith(
            query=merge_queries(self._url_parser.query, options.get('query', {})))
        soup = BeautifulSoup((self._pbrowser.get_content(
            url=_url_parser.full_url, **options)), 'html.parser')
        return soup

    def select(self, selector: str, namespaces: t.Any = None, limit: t.Optional[t.Any] = None, options: t.Dict[str, t.Any] = {}, **kwargs) -> ResultSet:
        ''' Perform a CSS selection operation on the current element.
        This uses the SoupSieve library.
        :param selector: A string containing a CSS selector.
        :param namespaces: A dictionary mapping namespace prefixes
            used in the CSS selector to namespace URIs. 
            By default, Beautiful Soup will use the prefixes 
            it encountered while parsing the document.
        :param limit: After finding this number of results, stop looking.
        :param kwargs: Keyword arguments to be passed into SoupSieve's
            soupsieve.select() method.
        :return: A ResultSet of Tags.
        :rtype: :class:`bs4.element.ResultSet`.
        '''
        soup = self.soup(options)
        result_set = soup.select(
            selector, namespaces=namespaces, limit=limit, **kwargs)
        return result_set

    def select_one(self, selector: str, namespaces: t.Any = None, options: t.Dict[str, t.Any] = {}, **kwargs) -> Tag:
        ''' Perform a CSS selection operation on the current element.
        :param selector: A CSS selector.
        :param namespaces: A dictionary mapping namespace prefixes
            used in the CSS selector to namespace URIs. 
            By default, Beautiful Soup will use the prefixes 
            it encountered while parsing the document.
        :param kwargs: Keyword arguments to be passed into SoupSieve's
            soupsieve.select() method.
        :return: A Tag.
        :rtype: :class:`bs4.element.Tag`.
        '''
        soup = self.soup(options)
        tag = soup.select_one(selector, namespaces=namespaces, **kwargs)
        return tag
