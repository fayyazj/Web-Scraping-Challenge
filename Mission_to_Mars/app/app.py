#IMPORT DEPENDENCIES
import pymongo
from flask import Flask, render_template
from scrape_mars import scrape

# PyMongo Setup
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.MarsDB

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def displaydata():
    data = list(db.posts.find())[-1]
    return render_template("index.html", data=data)

@app.route("/scrape")
def flaskscrape():
    scrapings = scrape()
    #posts = db.posts
    db.posts.insert_one(scrapings)
    return "Scraping complete."
    
if __name__ == '__main__':
    app.run(debug=True)