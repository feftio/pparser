import pparser

# https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=priceup&xsubject=128&page=1
# https://www.wildberries.ru/catalog/0/search.aspx?xfilters=xsubject%3Bdlvr%3Bbrand%3Bprice%3Bkind%3Bcolor%3Bwbsize%3Bseason%3Bconsists&xparams=preset%3D10948169&xshard=presets%2Fbucket_114&page=1&search=%D0%A1%D0%B8%D0%BC%D0%BF%D0%BB+%D0%B4%D0%B8%D0%BC%D0%BF%D0%BB&xsubject=1065%3B297%3B227&utm_source=vkentryprofit&click_id=v1_307801332

url = 'https://emoda.kz/'
pp = pparser.PParser(url=url)

soups = pp.get_soups(
    selector='div.list-popular-item',
    waitable_selector='img[src="https://emoda.kz/assets/resource/product/small_48911a.jpg"]'
)

print(len(soups))
