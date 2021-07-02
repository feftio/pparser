from product_parser import ProductParser

# https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=priceup&xsubject=128&page=1'

url = 'https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=priceup&xsubject=128&page=1'

parser = ProductParser(url=url)
products = parser.get_products({
    'page': 8
})

print(len(products))