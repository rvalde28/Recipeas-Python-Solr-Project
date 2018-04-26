import scrapy
import time
from fastfood.items import FastfoodItem
from fastfood.items import NutritionInfo


#scrapy crawl food -o ingredient.json

class foodSpider(scrapy.Spider):
    name = "food"
    start_urls = []

    def parse(self, response):
        allowed_domain = ["calorieking.com"]
        #restName = response.css('div.readable div.section-index div div ul li a')
        item = []
        item = FastfoodItem()

        #jsonresponse = json.loads(response.body_as_unicode())
        #get restaurant name
        item['restaurantName'] = response.css('#food-info ol li a::text').extract_first()
        #item['restaurantName'] = jsonresponse[response.css('#food-info ol li a::text').extract_first()]
        item['category'] = "fast food";

        #get what type of food this is 'beverage' 'dinner' etc
        kind = response.css('#food-info ol li a')[1]
        item['foodType'] = kind.css('::text').extract_first()

        #get the food item
        name = response.css('#food-info ol li')[2]
        item['foodItem'] = name.css('li::text').extract_first()
    
        info = []
        nutri = NutritionInfo()
        #get calories
        nutri['calories'] = response.css('tr.energy td.calories span.amount::text').extract_first()
    
        #get calories from fat
        nutri['caloriesFromFat'] = response.css('tr.fat-calories td span.amount::text').extract_first()

        #get total fat
        nutri['totalFat'] = response.css('tr.total-fat td.amount::text').extract_first()
        #get sat fat
        nutri['satFat'] = response.css('tr.sat-fat td.amount::text').extract_first()
        #get trans fat
        nutri['transFat'] = response.css('tr.trans-fat td.amount::text').extract_first()
        #get cholesterol
        nutri['cholesterol'] = response.css('tr.cholesterol td.amount::text').extract_first()
        #get sodium
        nutri['sodium'] = response.css('tr.sodium td.amount::text').extract_first()

        #get total carbs
        nutri['totalCarbs'] = response.css('tr.total-carbs td.amount::text').extract_first()
        #dietary fiber
        nutri['dietaryFiber'] = response.css('tr.fiber td.amount::text').extract_first()

        #get sugars
        nutri['sugars'] = response.css('tr.sugars td.amount::text').extract_first()

        #get sugar alcohol
        nutri['sugarAl'] = response.css('tr.sugar-alcohol td.amount::text').extract_first()    

        #get protein
        nutri['protein'] = response.css('tr.protein td.amount::text').extract_first()

        #get calcium
        nutri['calcium'] = response.css('tr.calcium td.amount::text').extract_first()

        #get potassium
        nutri['potassium'] = response.css('tr.potassium td.amount::text').extract_first()

        info.append(nutri)
        item['nutritionInfo'] = nutri
        amount = response.css('input#amount ::attr(value)').extract_first()
        size = response.css('select#units option::text').extract_first()

        item['serving_size'] = amount + ' ' + size

        yield item 
