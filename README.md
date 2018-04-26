# CSCE-470-Project

To run the spider you need to install scrapy(recommend using linux as it is easier to install and run)
command to run the spider:

scrapy crawl food -o ingredients.json

This will create a ingredients.json file that will contain the ingredients and other information for a recipe

Using Apache Solr as the database. Run the solr data base by going to the bin file in Solr
then do "./solr start" this will start the Apache Solr database

To run the python script you use python 3. It may ask for modules to be installed such as flask,
json simple. To run the website run the python script via "python3 client.py". Then open the link
that is displayed on the terminal. It should be "http://0.0.0.0:3000/". The website will show 
on the browser.
