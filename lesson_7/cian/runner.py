from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from cian import settings
from cian.spiders.cianru import CianruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # search = input()

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(CianruSpider)

    process.start()
