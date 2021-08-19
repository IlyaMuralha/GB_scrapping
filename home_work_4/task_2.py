from lxml import html
import requests
from pprint import pprint

from pymongo import MongoClient

my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.131 Safari/537.36'}
url = 'https://yandex.ru/news'

client = MongoClient('127.0.0.1', 27017)
db = client['news_sites']
collect_news = db.news

response = requests.get(url, headers=my_headers)
dom = html.fromstring(response.text)

parse_news = 'Яндекс новости'

items_news = dom.xpath('//a[contains(@href, "rubric=Tyumen") and @class="mg-card__link"]/ancestor::article')

ya_news = []
for item in items_news:
    news = {}
    title_news = item.xpath('.//h2[@class="mg-card__title"]/text()')
    annotation_news = item.xpath('.//div[@class="mg-card__annotation"]/text()')
    link_news = item.xpath('.//a[contains(@href, "rubric=Tyumen") and @class="mg-card__link"]/@href')
    dt_news = item.xpath('.//span[@class="mg-card-source__time"]/text()')
    source_news = item.xpath('.//a[contains(@href, "rubric=Tyumen") and @class="mg-card__source-link"]/@aria-label')

    news['title'] = str(title_news).replace('[', '').replace(']', '').replace("'", "").replace('\\xa0', ' ')
    news['annotation'] = str(annotation_news).replace('[', '').replace(']', '').replace("'", "")
    news['link'] = str(link_news).replace('[', '').replace(']', '').replace("'", "")
    news['datetime'] = str(dt_news).replace('[', '').replace(']', '').replace("'", "")
    news['source'] = str(source_news).replace('[', '').replace(']', '').replace("'", "")
    news['source_pars'] = parse_news
    ya_news.append(news)

pprint(ya_news)
pprint(len(ya_news))

for news in ya_news:
    collect_news.update_one(
        {'link': news['link']},
        {'$set': news},
        upsert=True
    )

for doc in collect_news.find({}):
    pprint(doc)
