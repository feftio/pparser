from product_parser import ProductParser

# https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=priceup&xsubject=128&page=1'

url = 'https://www.wildberries.ru/catalog/0/search.aspx?xfilters=xsubject%3Bdlvr%3Bbrand%3Bprice%3Bkind%3Bcolor%3Bwbsize%3Bseason%3Bconsists&xparams=preset%3D10948169&xshard=presets%2Fbucket_114&page=1&search=%D0%A1%D0%B8%D0%BC%D0%BF%D0%BB+%D0%B4%D0%B8%D0%BC%D0%BF%D0%BB&xsubject=1065%3B297%3B227&utm_source=vkentryprofit&click_id=v1_307801332'
parser = ProductParser(url=url)

products = parser.get_products(query={
    'page': 1
}, wait_for_selector='.dtList-inner')
print(len(products))
