from lxml import html
import requests
from pprint import pprint


url = 'https://ru.ebay.com/b/Comic-Books-Manga-Memorabilia/63/bn_1865459'
my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.131 Safari/537.36'}
my_params = ''

response = requests.get(url, headers=my_headers)

dom = html.fromstring(response.text)

items = dom.xpath('//li[contains(@class, "s-item")]')

magazines = []
for item in items:
    magazine = {}
    name = item.xpath('.//h3[@class="s-item__title"]/text()')
    link = item.xpath('.//a[@class="s-item__link"]/@href')
    price = item.xpath('.//span[@class="s-item__price"]//text()')
    info = item.xpath('.//span[contains(@class, "s-item__hotness")]//text()')

    magazine['name'] = name
    magazine['link'] = link
    magazine['price'] = price
    magazine['info'] = info

    magazines.append(magazine)

pprint(magazines)
