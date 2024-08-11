# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    product_link = scrapy.Field()
    stars = scrapy.Field()
    bought_in_past_month = scrapy.Field()
