from bs4 import BeautifulSoup
import requests

from splinter import Browser
import pandas as pd

from flask import Flask, render_template, render_template
from flask_pymongo import pymongo
import scrape_mars

#################################################
# Database Setup
#################################################
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", info=mars_data)

@app.route("/scrape")
def scrape():
    mars_info = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)