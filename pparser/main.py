from __future__ import annotations

from bs4.element import ResultSet
from pparser.pbrowser import PBrowser
import typing as t

from bs4 import BeautifulSoup
from pyppeteer import launch
from pyppeteer.browser import Browser

from pparser.product import Product
from pparser.utils import merge_queries
from pparser.url_parser import UrlParser


class PParser:

    def __init__(self, url: str, **options):
        self._url_parser = UrlParser(url)
        self._pbrowser = PBrowser(**options)

    def soup(self, **options) -> BeautifulSoup:
        _url_parser = self._url_parser.copywith(
            query=merge_queries(self._url_parser.query, options.get('query', {})))
        soup = BeautifulSoup((self._pbrowser.get_content(
            url=_url_parser.full_url, **options)), 'html.parser')
        return soup

    def select(self, selector: str, **options) -> ResultSet:
        soup = self.soup(**options)
        soups = soup.select(selector)
        return soups

        # for soup_product in soup_products:
        #     discount = soup_product.find('span', class_='price-sale active')
        #     discount = discount.get_text(strip=True) if discount else ''

        #     products.append(
        #         Product(
        #             brand=soup_product.find(
        #                 'strong', class_='brand-name c-text-sm').get_text(strip=True).replace('/', ''),
        #             title=soup_product.find(
        #                 'span', class_='goods-name c-text-sm').get_text().split('/')[0],
        #             price=soup_product.find(
        #                 class_='lower-price').get_text(strip=True).replace('\xa0', '').replace('₽', ''),
        #             discount=discount,
        #             link=_url_parser.root_url +
        #             soup_product.find(
        #                 'a', class_='ref_goods_n_p j-open-full-product-card').get('href')
        #         )
        #     )
        # return products
