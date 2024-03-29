from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroy import settings
from leroy.spiders.leroyru import LeroyruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # search = input()

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyruSpider)

    process.start()
