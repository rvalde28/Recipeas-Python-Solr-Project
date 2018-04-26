# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy.item import Item, Field

class FoodnetworkspiderItem(Item):
    # define the fields for your item here like:
    recipe_name = Field()
    ingredients = Field()
    directions = Field()
    nutrition_facts = Field()
    total_ratings = Field()
    ratings = Field()
    prep_time = Field()
    cook_time = Field()
    ready = Field()
    img = Field()

