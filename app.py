from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__) # set up Flask

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/") # tells Flask what to display when we're looking at the home page
def index():
   mars = mongo.db.mars.find_one() # uses PyMongo to find the "mars" collection in our database
   return render_template("index.html", mars=mars) # return an HTML template using an index.html file

# access the database, scrape new data
@app.route("/scrape") # route that Flask will be using
def scrape():
   mars = mongo.db.mars # a new variable that points to our Mongo database
   mars_data = scraping.scrape_all() # new variable to hold the newly scraped data
   mars.update_one({}, {"$set":mars_data}, upsert=True) #  update the database 
   return redirect('/', code=302)


if __name__ == "__main__":
   app.run()