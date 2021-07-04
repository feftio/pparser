from __future__ import annotations
import typing as t

from copy import deepcopy
from url_parser import UrlParser

from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch
from pyppeteer.browser import Browser

import requests
import requests_html

from urllib.parse import ParseResult, urlparse, parse_qsl, urlencode, urlunparse
from product import Product


async def launch_browser():
    return await launch(headless=True, ignoreHTTPSErrors=False, args=[
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--disable-setuid-sandbox',
        '--no-first-run',
        '--no-sandbox',
        '--no-zygote',
        '--deterministic-fetch',
        '--disable-features=IsolateOrigins',
        '--disable-site-isolation-trials'
    ],)


class ProductParser(UrlParser):

    def __init__(self, url: str, verify: bool = True, visible: bool = False):
        super().__init__(url)
        self.browser: Browser = asyncio.get_event_loop().run_until_complete(launch_browser())

    async def get_content(self, url: str, selector: t.Optional[str] = None):
        page = await self.browser.newPage()
        await page.goto(url, options={'timeout': int(8 * 1000)})
        if not(selector is None):
            await page.waitForSelector(selector)
        return await page.content()

    def get_products(self, query: t.Dict[str, t.Any] = {}, wait_for_selector: t.Optional[str] = None) -> t.List[Product]:
        _query = urlencode({**dict(parse_qsl(self.query)), **query})
        _url = self.copywith(query=_query)

        products = []

        soup = BeautifulSoup(asyncio.get_event_loop().run_until_complete((self.get_content(url=_url.full_url, selector=wait_for_selector))), 'html.parser')
        soup_products = soup.findAll('div', class_='dtList-inner')

        for soup_product in soup_products:
            discount = soup_product.find('span', class_='price-sale active')
            discount = discount.get_text(strip=True) if discount else ''

            products.append(
                Product(
                    brand=soup_product.find(
                        'strong', class_='brand-name c-text-sm').get_text(strip=True).replace('/', ''),
                    title=soup_product.find(
                        'span', class_='goods-name c-text-sm').get_text().split('/')[0],
                    price=soup_product.find(
                        class_='lower-price').get_text(strip=True).replace('\xa0', '').replace('₽', ''),
                    discount=discount,
                    link=_url.root_url +
                    soup_product.find(
                        'a', class_='ref_goods_n_p j-open-full-product-card').get('href')
                )
            )
        return products
