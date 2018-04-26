#! /usr/bin/python3

from flask import Flask, render_template, request,url_for
from urllib.request import urlopen

import cgi
import random
import simplejson

app = Flask(__name__)
solr_port = 8983


solr_link = []
html_counter = [-1]


class recipe(object):

	def __init__(self, recipename, preptime, calories, imgaddress):
		self.name = recipename
		self.prep = preptime
		self.cal = calories
		self.imgadr = imgaddress

def parse_calories(nutr_list):
    for fact in nutr_list:
        if 'calories' in fact:
            return int(fact.split(' ')[0])

def parse_time(time_list):
    time = 0
    for unit in time_list:
        if 'h' in unit:
            time += 60*int(unit.split(' ')[0])
        elif 'm' in unit:
            time += int(unit.split(' ')[0])

    return time

@app.route('/')
def index():
    return render_template('index.html')

#form for the results from the main page
#gets the results from the user and connects
#to the solr database to make the query
@app.route('/results', methods=['POST'])
def results():
    start = 0
    rows = 10
    ing_include = request.form['ing_include']
    ing_exclude = request.form['ing_exclude']
    spec_time = request.form['prep_time']
    spec_cal = request.form['calories']

    #current database is localhosted via port 8983
    url_query = "http://localhost:" + str(solr_port) + "/solr/recipeas/select?q="

    ing_include_list = ing_include.split(", ")
    ing_exclude_list = ing_exclude.split(", ")

    if len(ing_include_list) > 0 and ing_include_list[0] != '':
        for ing in ing_include_list:
            url_query = url_query + "%2Bingredients:" + ing + "%20"

    if len(ing_exclude_list) > 0 and ing_exclude_list[0] != '':
        for ing in ing_exclude_list:
            url_query = url_query + "-ingredients:" + ing + "%20"

    #makes connections to solr database
    connection = urlopen(url_query)
    response = simplejson.load(connection)
    maxDocs = response['response']['numFound']

    #selects up to 10 random results based on response
    start = random.randint(0,maxDocs-11)
    startString = "&rows="+ str(rows) +"&start="+ str(start)
    

    connection = urlopen(url_query + startString)
    response = simplejson.load(connection)

    solr_link.append(url_query + startString)
    html_counter.append(html_counter[0]+1)

    #gets the the ready information, recipe name, the image from the query
    #then it calls a template to render this information to the html page
    recipes = []
    for doc in response['response']['docs']:
        calories = parse_calories(doc['nutrition_facts'])
        if spec_cal != '' and calories > int(spec_cal):
            continue

        if 'ready' in doc:
            ready_time = parse_time(doc['ready'])
        else:
            ready_time = -1
        if spec_time != '' and ready_time > int(spec_time):
            continue

        recipe_name = doc['recipe_name'][0]
        image_url = doc['img'][0]
        if ready_time != -1:
            recipes.append(recipe(recipe_name, ready_time, calories, image_url))
        else:
            recipes.append(recipe(recipe_name, '', calories, image_url))

    #renders the template results.html
    return render_template('results.html', recipes = recipes, img_width = 200, img_height = 100)

#used to get the selected recipe the user wants more information of
#gets results via button selected the returns the result as an html page
@app.route("/selection",methods=['GET','POST'])
def selection():
    print(request.method)
    if (request.method == 'POST'):
        if (request.form.get('0') == 'Get this Recipe!'):
            print (solr_link)
            number = 0
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('1') == 'Get this Recipe!'):
            print ("2")
            number = 1
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('2') == 'Get this Recipe!'):
            print ("3")
            number = 2
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('3') == 'Get this Recipe!'):
            print ("4")
            number = 3
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('4') == 'Get this Recipe!'):
            print ("5")
            number = 4
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('5') == 'Get this Recipe!'):
            print ("6")
            number = 5
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('6') == 'Get this Recipe!'):
            print ("7")
            number = 6
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('7') == 'Get this Recipe!'):
            print ("8")
            number = 7
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('8') == 'Get this Recipe!'):
            print ("9")
            number = 8
            html_code = getRecipe(number)
            return html_code

        elif (request.form.get('9') == 'Get this Recipe!'):
            print ("10")
            number = 9
            html_code = getRecipe(number)
            return html_code
        else:
            return render_template('index.html')

#gets the recipe that the user clicked on 
def getRecipe(number):
    counter = 0
    recipeName = ''
    ingredients = []
    nutritionFacts = []
    ready = []
    img = ''
    directions = []
    connection = urlopen(solr_link[html_counter[0]])
    response = simplejson.load(connection)

    for document in response['response']['docs']:
        if(counter == number):
            print ("found")
            recipeName = document['recipe_name'][0]
            ingredients = document['ingredients']
            nutritionFacts = document['nutrition_facts']
            if ('ready' in document):
                ready = document['ready']            
            img = document['img'][0]
            directions = document['directions']
        counter+=1

    #renders title for the recipe
    htmlRecipe = '<div> <h1>%s</h1> </div>' % (str(recipeName))

    #gets the size of the image if there is an image
    width = 0
    height = 0
    temp_str = ''
    if(len(img)>0):
        back = 0
        size_str = ''
        for char in img:
            if (back == 4 and char != '/'):
                size_str = size_str + char
            if (char == '/'):
                back = back + 1

        for char in size_str:
            if(char != 'x' and width == 0):
                temp_str = temp_str + char
            elif(char == 'x'):
                print (temp_str)
                width = int(temp_str)
                temp_str = ''
            elif(char != 'x' and (width > 0)):
                temp_str = temp_str + char

        height = int(temp_str)

    #makes the html source code for the entire recipe
    #things it displays are the recipe name, the image, the ingredients 
    #the directions, and nutritional facts
    html_image = '<div> <iframe src="%s" width="%d" height = "%d"> </iframe> </div>' % (str(img), width, height)
    html_ing = ''
    for ingre in ingredients:
        html_ing = html_ing + '<div> <div style = "line-height: 1.6"> %s</div> </div>' % (str(ingre))
    duration = ''
    for time in ready:
        duration = duration + str(time)
   
    html_time = ''
    if (len(ready) > 0):
        html_time = '<h2>Ready in: </h2> <div> <div>%s</div</div>' % (str(duration))

    html_directions = ''
    counter = 1
    for direc in directions:
        html_directions = html_directions + '<div><div style = "line-height: 1.6">Step %d: %s</div></div>' % (counter,str(direc))
        counter = counter + 1

    html_nutri = ''
    for nutri in nutritionFacts:
        html_nutri = html_nutri + '<div><div style = "line-height: 1.6">%s</div></div>' % str(nutri)

    ingredientsTitle = '<h2>Ingredients: </h2>'
    Directions = '<h2>Directions: </h2>'
    Nutritional = '<h2>Nutritional Facts: </h2>'

    return htmlRecipe + '<br/>' +  html_image + '<br/>'+ ingredientsTitle + '<br/>'  + html_ing + '<br/>'+ html_time + '<br/>' + '<br/>'+ Directions +  html_directions  + Nutritional +  html_nutri

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
