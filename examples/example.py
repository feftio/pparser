import pparser

# https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=priceup&xsubject=128&page=1
# https://www.wildberries.ru/catalog/0/search.aspx?xfilters=xsubject%3Bdlvr%3Bbrand%3Bprice%3Bkind%3Bcolor%3Bwbsize%3Bseason%3Bconsists&xparams=preset%3D10948169&xshard=presets%2Fbucket_114&page=1&search=%D0%A1%D0%B8%D0%BC%D0%BF%D0%BB+%D0%B4%D0%B8%D0%BC%D0%BF%D0%BB&xsubject=1065%3B297%3B227&utm_source=vkentryprofit&click_id=v1_307801332

url = 'https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=priceup&xsubject=128&page=1'
pp = pparser.PParser(url=url)
pp.set_options()
for item in pp.select(selector='div.dtList-inner'):
    print(item.select_one('strong.brand-name.c-text-sm').string)  # brand
    print(item.select_one('span.goods-name.c-text-sm').string)  # title
    print(item.select_one('.lower-price').string)  # price
    print(item.select_one('span.price-sale.active').string)  # discount
    print(item.select_one('a.ref_goods_n_p.j_open_full-product-card').href)  # link
    print('---------------------------')

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
