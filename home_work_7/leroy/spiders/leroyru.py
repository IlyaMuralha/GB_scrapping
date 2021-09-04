import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroy.items import LeroyItem


class LeroyruSpider(scrapy.Spider):
    name = 'leroyru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/mebel/']
    url = 'https://leroymerlin.ru'

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//div[@data-qa-pagination]//a[@data-qa-pagination-item="right"]/@href'
        ).extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//div[@data-qa-product]/a/@href')
        for link in links:
            yield response.follow(link, callback=self.product_parse)
        print()

    def product_parse(self, response: HtmlResponse):
        print()
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('name', '//h1//text()')
        print()
        pass
