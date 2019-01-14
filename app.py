import os
from flask import Flask, app, redirect, url_for, render_template, request, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from config import mongo_uri, mongodb

app = Flask(__name__)
app.config["MONGO_DBNAME"] = mongodb()
app.config["MONGO_URI"] = mongo_uri()

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("index.html")


@app.route('/<user>')
def profile(user):
    return render_template("index.html")


@app.route('/all_stories')
def all_stories():
    return render_template("allstories.html", 
    stories=mongo.db.stories.find())


@app.route('/search')
def search():
    return render_template("index.html")


@app.route('/story')
def story():
    return render_template("story.html", 
    stories=mongo.db.stories.find())


@app.route('/new_story')
def new_story():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host=os.getenv("IP"),
            port=os.getenv("PORT"),
            debug=True)
