from product_parser import ProductParser

# https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=priceup&xsubject=128&page=1'

url = 'https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=priceup&xsubject=128&page=1'

parser = ProductParser(url=url)

pages = []
for page in range(1, 9):
    products = parser.get_products({
    'page': page
    })
    pages.append(products)

print(len(pages))