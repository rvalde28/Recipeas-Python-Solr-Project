# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class FastfoodItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = Field()
    restaurantName = Field()
    foodType = Field()
    foodItem = Field()
    nutritionInfo = Field()

class NutritionInfo(scrapy.Item):
    calories = Field()
    caloriesFromFat = Field()
    totalFat = Field()
    satFat = Field()
    transFat = Field()  
    cholesterol = Field()
    sodium = Field()
    totalCarbs = Field()
    dietaryFiber = Field()
    sugars = Field()
    sugarAl = Field()
    protein = Field()
    calcium = Field()
    potassium = Field()
