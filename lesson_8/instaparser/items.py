# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    user_id = scrapy.Field()
    username = scrapy.Field()
    picture_profile_url = scrapy.Field()
    data_owner_public = scrapy.Field()
    data_post = scrapy.Field()
    picture_post_url = scrapy.Field()
    comments = scrapy.Field()
    count_comments = scrapy.Field()
    likes = scrapy.Field()
    accessibility_caption = scrapy.Field()
    _id = scrapy.Field()

