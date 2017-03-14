# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyBookingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    hotel_id = scrapy.Field()
    rating_word = scrapy.Field()
    rating_score = scrapy.Field()
    star_rating = scrapy.Field()
    location_bbox = scrapy.Field()
    location_coords = scrapy.Field()
    location_address = scrapy.Field()
    reviews = scrapy.Field()
    pass
