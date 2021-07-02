from __future__ import annotations
import typing as t
import requests
from urllib.parse import ParseResult, urlparse, parse_qsl
from bs4 import BeautifulSoup
from product import Product


class ProductParser:

    def __init__(self, url: str):
        self._headers: t.Dict[str, str] = {
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'accept': '*/*'
        }
        self._url: ParseResult = urlparse(url)

    @property
    def full_url(self) -> str:
        return self._url.geturl()

    @property
    def root_url(self) -> str:
        return f'{self._url.scheme}://{self._url.netloc}'

    @property
    def url(self) -> str:
        return f'{self._url.scheme}://{self._url.netloc}{self._url.path}'

    def get_products(self, params: t.Dict[str, t.Any] = {}) -> t.List[Product]:
        params = {**dict(parse_qsl(self._url.query)), **params}
        response = requests.get(self.url, headers=self._headers, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')

        products = []
        soup_products = soup.findAll('div', class_='dtList-inner')

        for soup_product in soup_products:
            discount = soup_product.find('span', class_='price-sale active')
            discount = discount.get_text(strip=True) if discount else ''

            products.append(
                Product(
                brand=soup_product.find('strong', class_='brand-name c-text-sm').get_text(strip=True).replace('/', ''),
                title=soup_product.find('span', class_='goods-name c-text-sm').get_text().split('/')[0],
                price=soup_product.find(class_='lower-price').get_text(strip=True).replace('\xa0', '').replace('₽', ''),
                discount=discount,
                link=self.root_url + soup_product.find('a', class_='ref_goods_n_p j-open-full-product-card').get('href')
                )
            )
        return products
