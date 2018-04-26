import scrapy
import time
from foodNetworkSpider.items import FoodnetworkspiderItem


#scrapy crawl food -o ingredient.json

class Gen():
    def generate_URL(self):
        url_list = []
        for i in range(0, 100000):
            url_list.append('http://allrecipes.com/recipe/'+str(0+i) + '/')
        return url_list

class QuotesSpider(scrapy.Spider):
    q = Gen()
    name = "food"
    start_urls = q.generate_URL()

    def parse(self, response):
        #time.sleep(2.5)
        title = response.css("section")    
        
        item = []
        item = FoodnetworkspiderItem()
        item['recipe_name'] = title.css("section h1.recipe-summary__h1::text").extract_first()

        #ADD INGREDIENTS
        ing = []        
        quote = response.css("ul li label span.recipe-ingred_txt::text").extract()
        for i in range(len(quote)):
            ing.append(quote[i])
            if(i == (len(quote)-3)):
                break

        item['ingredients'] = ing
            
        #ADD DIRECTIONS
        direc = []
        for direct in response.css("ol li.step span"):
            direc.append(direct.css("::text").extract_first())
        item['directions'] = direc

        #nutritional facts
        nutri = []
        ext = response.css("section.recipe-footnotes div::text").extract(); 
        ext = [x.rstrip() for x in ext]  
        ext.pop(0)
        ext.pop(0)
        for x in range(len(ext)):
            ext[x] = ext[x].replace(',', '')
            ext[x] = ext[x].replace(';', '')
            
        info = response.css("section.recipe-footnotes div span::text").extract()
        for x in range(len(info)):
            info[x] = info[x].replace(';','')


        for i in range(len(info)):
            if(i == 0):
                continue
            elif(i == (len(info)-2)):
                break
            else:
                nutri.append(info[i]+ext[i])

        item['nutrition_facts'] = nutri

        #total ratings
        item['total_ratings'] = response.css("ol li h4.helpful-header::text").extract_first()

        #ratings
        rat = []
        rat = response.css("ol li div::attr(title)").extract()
        
        item['ratings'] = rat

        prep_ext =response.css('time[itemprop=prepTime]::text').extract()
        prep = response.css('time[itemprop=prepTime] span::text').extract()
        prep = [str(x[0]) + x[1] for x in zip(prep, prep_ext)]

        cook_ext = response.css('time[itemprop=cookTime]::text').extract()
        cook = response.css('time[itemprop=cookTime] span::text').extract()
        cook = [str(x[0]) + x[1] for x in zip(cook, cook_ext)]

        ready_ext = response.css('time[itemprop=totalTime]::text').extract()
        ready = response.css('time[itemprop=totalTime] span::text').extract()
        ready = [str(x[0]) + x[1] for x in zip(ready, ready_ext)]

        item['prep_time'] = prep
        item['cook_time'] = cook
        item['ready'] = ready
        item['img'] = response.css('img.rec-photo ::attr(src)').extract_first()

        return item

