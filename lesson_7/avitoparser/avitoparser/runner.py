from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser.avitoparser import settings
from avitoparser.avitoparser.spiders.avito import AvitoSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # search = input()

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoSpider, search='велосипед')

    process.start()
