import os
from flask import Flask, app, redirect, url_for, render_template, request, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from config import mongo_uri, mongodb, secret_key, test_user
from slugify import slugify

app = Flask(__name__)
app.config["MONGO_DBNAME"] = mongodb()
app.config["MONGO_URI"] = mongo_uri()
app.config["SECRET_KEY"] = secret_key()

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("index.html")


@app.route('/login')
def login():
    session["username"] = test_user()
    return redirect(url_for('profile', user=session['username']))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/profile/<user>')
def profile(user):
    profile=mongo.db.users.find({'user_name': user})
    stories=mongo.db.stories.find({'author': user})
    return render_template("profile.html", user=user, stories=stories, profile=profile)


@app.route('/editprofile/<user>')
def edit_profile(user):
    profile=mongo.db.users.find({'user_name': user})
    return render_template("editprofile.html", user=user, profile=profile)
    


@app.route('/all_stories')
def all_stories():
    return render_template("allstories.html", 
    stories=mongo.db.stories.find())


@app.route('/search')
def search():
    return render_template("index.html")


@app.route('/read/<story_to_read>/<chapter_number>')
def read(story_to_read, chapter_number):
    stories=mongo.db.stories.find()
    chapter_index=int(chapter_number) - 1
    for story in stories:
        if story_to_read == story['url']:
            author = story['author']
            title = story['title']
            fandom = story['fandom']
            summary = story['summary']
            total_chapters = len(story['chapters'])
            chapter = story['chapters'][chapter_index]
    return render_template("story.html", story=story_to_read, title=title, author=author, fandom=fandom, summary=summary, total_chapters=total_chapters, chapter=chapter, chapter_number=chapter_number)


@app.route('/new_story')
def new_story():
    return render_template("newstory.html")


if __name__ == "__main__":
    app.run(host=os.getenv("IP"),
            port=os.getenv("PORT"),
            debug=True)
