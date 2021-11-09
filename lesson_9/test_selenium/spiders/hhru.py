import scrapy
from scrapy.http import HtmlResponse
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=Python+junior&from=suggest_post']

    # def start_requests(self):
    #     if not self.start_urls and hasattr(self, 'start_url'):
    #         raise AttributeError(
    #             "Crawling could not start: 'start_urls' not found "
    #             "or empty (but found 'start_url' attribute instead, "
    #             "did you miss an 's'?)")
    #     for url in self.start_urls:
    #         yield SeleniumRequest(url=url)
    #
    # def parse(self, response:HtmlResponse):
    #     next_page = response.xpath('//a[@data-qa="pager-next"]/@href').extract_first()
    #     if next_page:
    #         yield SeleniumRequest(
    #                 url=next_page,
    #                 callback=self.parse,
    #             )

    def parse(self, response: HtmlResponse):
        # vacancies = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]')
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse_result,
            wait_time=10,
            wait_until=EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="pager-next"]'))
        )

        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').extract_first()
        if next_page:
            yield SeleniumRequest(
                    url=next_page,
                    callback=self.parse_result,
                )
        print()

    def parse_result(self, response: HtmlResponse):
        vacancies_links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]')
        print()
