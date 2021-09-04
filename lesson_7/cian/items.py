import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def clear_price(value):
    value = value.replace('\xa0', '').replace('₽', '')
    try:
        return int(value)
    except:
        return value


def change_uri(value):
    return value.replace('-2.jpg', '-1.jpg')


class CianItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    currency = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(change_uri))
    _id = scrapy.Field()
