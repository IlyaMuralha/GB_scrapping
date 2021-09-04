import scrapy
from scrapy.http import HtmlResponse
from avitoparser.avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    def __init__(self, search):
        super(AvitoSpider, self).__init__()
        self.start_urls = [f'https://www.avito.ru/tyumen?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-marker="item-title"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath('name', '//h1/span/text()')
        loader.add_xpath('photos', '//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_xpath('price',
                         '//span[contains(@class, "price-value-string")]/span[contains(@itemprop, "price")]/text()')
        loader.add_value('url', response.url)
        loader.add_value('site_name', self.allowed_domains[0])

        yield loader.load_item()

        # name = response.xpath('//h1/span/text()').extract_first()
        # price = response.xpath(
        #     '//span[contains(@class, "price-value-string")]/span[contains(@itemprop, "price")]/text()'
        # ).extract_first()
        # photos = response.xpath('//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        # yield AvitoparserItem(name=name, photos=photos)
