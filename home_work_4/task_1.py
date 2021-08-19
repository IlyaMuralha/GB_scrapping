from lxml import html
import requests
from pprint import pprint

from pymongo import MongoClient

my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.131 Safari/537.36'}
url = 'https://lenta.ru/'

client = MongoClient('127.0.0.1', 27017)
db = client['news_sites']
collect_news = db.news

response = requests.get(url, headers=my_headers)
dom = html.fromstring(response.text)

source_news = 'Лента.ру'

items_news = dom.xpath('//section[contains(@class, "row")][1]//div[contains(@class, "item")]')

lenta_news = []
for item in items_news:
    news = {}
    text_news = item.xpath('.//a[1]/text()')
    link_news = item.xpath('./a[1]/@href')
    dt_news = item.xpath('.//time[@class="g-time"]/@datetime')

    news['text'] = str(text_news).replace('[', '').replace(']', '').replace("'", "").replace('\\xa0', ' ')
    news['link'] = url + str(link_news).replace('[', '').replace(']', '').replace("'", "")
    news['datetime'] = str(dt_news).replace('[', '').replace(']', '').replace("'", "")
    news['source'] = source_news

    lenta_news.append(news)

pprint(lenta_news)
pprint(len(lenta_news))

for news in lenta_news:
    collect_news.update_one(
        {'link': news['link']},
        {'$set': news},
        upsert=True
    )

for doc in collect_news.find({}):
    pprint(doc)
