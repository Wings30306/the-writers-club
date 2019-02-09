import os
import json
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


@app.route('/<user>')
def profile(user):
    profile=mongo.db.users.find({'user_name': user})
    stories=mongo.db.stories.find({'author': user})
    return render_template("profile.html", user=user, stories=stories, profile=profile)


@app.route('/<user>/edit')
def edit_profile(user):
    profile=mongo.db.users.find({'user_name': session['username']})
    if user == session['username']:
        return render_template("editprofile.html", user=user, profile=profile)
    else:
        flash("You cannot edit someone else's profile!")
        return redirect(url_for('profile', user=user, profile=profile))
    
@app.route('/<user>/edit', methods=['POST'])
def update_profile(user):
    if user == session['username']:
        users = mongo.db.users
        users.replace_one( {"user_name": user},
        {   
            "user_name": user,
            "birthday": request.form['birthday'],
            "date_started_writing": request.form['date_started_writing'],
            "intro": request.form['intro']
        })

        return redirect(url_for('profile', user = user)) 
    else:
        flash("You cannot edit someone else's profile!")
        return redirect(url_for('profile', user=user, profile=profile))
    


@app.route('/all_stories')
def all_stories():
    return render_template("allstories.html", 
    stories=mongo.db.stories.find())


@app.route('/search')
def search():
    return render_template("index.html")


@app.route('/<story_to_read>/<chapter_number>')
def read(story_to_read, chapter_number):
    stories=mongo.db.stories.find({"url": story_to_read})
    this_chapter = "chapter" + chapter_number
    for story in stories:
        if story_to_read == story['url']:
            author = story['author']
            title = story['title']
            fandom = story['fandom']
            disclaimer = story['disclaimer']
            summary = story['summary']
            chapter = story[this_chapter]
    return render_template("story.html", story=story_to_read, title=title, author=author, fandom=fandom, chapter=chapter, chapter_number=chapter_number, summary=summary, disclaimer=disclaimer)


@app.route('/<story_to_read>/<chapter_number>/edit')
def edit_chapter(story_to_read, chapter_number):
    stories=mongo.db.stories.find({"url": story_to_read}) 
    this_chapter = "chapter" + chapter_number
    for story in stories:
        if session['username'] == story['author']:
            chapter = story[this_chapter]
            return render_template("editstory.html", story=story_to_read, chapter=chapter, chapter_number=chapter_number)
        else:
            flash("You cannot edit someone else's story!")
            return redirect(url_for("index"))


@app.route('/<story_to_read>/<chapter_number>/edit', methods=['POST'])
def update_chapter(story_to_read, chapter_number):
    stories = mongo.db.stories
    title = request.form['chapter_title']
    chapter_updated = json.loads(request.form['editor'])
    chapter = "chapter" + chapter_number
    print(chapter_updated)
    stories.find_one_and_update( {"url": story_to_read},
    { "$set": {
        chapter:{'chapter_title': title,
        'chapter_content': chapter_updated }
    }
    })

    return redirect(url_for('read', story_to_read=story_to_read, chapter_number=chapter_number)) 

@app.route('/new_story')
def new_story():
    return render_template("newstory.html")


if __name__ == "__main__":
    app.run(host=os.getenv("IP"),
            port=os.getenv("PORT"),
            debug=True)
