from __future__ import annotations
import typing as t

from pyppeteer import browser

from pparser.url_parser import UrlParser

from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch
from pyppeteer.browser import Browser

from urllib.parse import ParseResult, urlparse, parse_qsl, urlencode, urlunparse
from pparser.product import Product

from pparser.utils import merge_queries

LAUNCH_ARGS = (
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-setuid-sandbox',
    '--no-first-run',
    '--no-sandbox',
    '--no-zygote',
    '--deterministic-fetch',
    '--disable-features=IsolateOrigins',
    '--disable-site-isolation-trials',
)

DEFAULT_HEADERS = {}


def run_async(awaitable):
    return asyncio.get_event_loop().run_until_complete(awaitable)


class PParser:

    def __init__(self, url: str, verify: bool = True, visible: bool = False, width: int = 1920, height: int = 1080):
        self._url_parser = UrlParser(url)
        self.width = width
        self.height = height
        self.browser: Browser = run_async(
            launch(headless=not(visible), ignoreHTTPSErrors=not(verify), args=(
                *LAUNCH_ARGS, f'--window-size={self.width},{self.height}')))

    async def get_content(self, url: str, waitable_selector: t.Optional[str] = None, timeout: int = 4000, sleep: float = 0.2):
        page = await self.browser.newPage()
        await page.setViewport({
            'width': self.width,
            'height': self.height,
        })
        await page.goto(url, options={'timeout': int(timeout)})
        if waitable_selector is not None:
            await page.waitForSelector(waitable_selector)
        await asyncio.sleep(sleep)
        await page.screenshot({'path': 'screenshot.png'})
        return await page.content()

    def get_products(self, query: t.Dict[str, t.Any] = {}, selector: str = '', timeout: int = 4000, sleep: float = 0.2) -> t.List[Product]:
        _url_parser = self._url_parser.copywith(
            query=merge_queries(self._url_parser.query, query))

        products = []

        soup = BeautifulSoup(run_async((self.get_content(
            url=_url_parser.full_url, waitable_selector=selector, timeout=timeout, sleep=sleep))), 'html.parser')
        soup_products = soup.select(selector)

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
                    link=_url_parser.root_url +
                    soup_product.find(
                        'a', class_='ref_goods_n_p j-open-full-product-card').get('href')
                )
            )
        return products
