from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import time

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():
    planet = mongo.db.mars_info
    mars_info = scrape_mars.scrape()
    planet.update({}, mars_info, upsert=True)
    time.sleep(5)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
