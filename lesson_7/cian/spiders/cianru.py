import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from cian.items import CianItem

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class CianruSpider(scrapy.Spider):
    name = 'cianru'
    allowed_domains = ['cian.ru']
    start_urls = ['https://cian.ru/kupit/']

    def parse(self, response: HtmlResponse):
        popular_category_pages = response.xpath(
            "//div[@class='c-popular-links']//a[contains(@class, 'c-popular-links-item')]/@href").extract()
        for url in popular_category_pages:
            yield response.follow(url, callback=self.ads_page_pars)

    def ads_page_pars(self, response: HtmlResponse):
        paginator = response.xpath('//div/ul//li[contains(@class, "list-item")]/a/@href').extract()
        for page in paginator:
            yield response.follow(page, callback=self.ads_page_pars)

        ads_links = response.xpath('//article//div[@data-name="LinkArea"]/a/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.ads_parse)
        pass

    def ads_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=CianItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@itemprop="price"]/text()')
        loader.add_xpath('currency', '//span[@itemprop="priceCurrency"]/@content')

        driver = webdriver.Chrome()
        driver.get(response.url)
        action = ActionChains(driver)
        cookie_button = driver.find_element_by_xpath('//span[contains(text(), "Принять")]')
        cookie_button.click()

        thumbs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@class,"fotorama__nav__frame--thumb")]')
            )
        )
        action.move_to_element(thumbs[-1]).click().perform()

        photos = [i.find_element_by_xpath(
            '//div[@class="fotorama__nav__frame fotorama__nav__frame--thumb"]//img'
        ).get_attribute("src") for i in thumbs]
        photos.pop()
        driver.quit()

        loader.add_value('photos', photos)
        print()
        yield loader.load_item()
