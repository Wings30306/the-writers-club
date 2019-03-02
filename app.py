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
    if session:
        profile=mongo.db.users.find({'user_name': user})
        if user == session['username']:
            return render_template("editprofile.html", user=user, profile=profile)
        else:
            flash("You cannot edit someone else's profile!")
            return redirect(url_for('profile', user=user, profile=profile))
    else:
        flash("You must be signed in to edit your profile.")
        return redirect(url_for("index"))
   

    
@app.route('/<user>/edit', methods=['POST'])
def update_profile(user):
    if session:
        if user == session['username']:
            users = mongo.db.users
            users.find_one_and_update( {"user_name": user},
            { "$set": 
            {   
                "user_name": user,
                "birthday": request.form.get('birthday'),
                "date_started_writing": request.form.get('date_started_writing'),
                "intro": json.loads(request.form.get('editor')),
                "show_birthday": request.form.get('show_birthday')
            }
            })
            return redirect(url_for('profile', user = user)) 
        else:
            flash("You cannot edit someone else's profile!")
            return redirect(url_for('profile', user=user, profile=profile))
    else: 
        flash("You must be signed in to edit your profile!")
        return redirect(url_for('profile', user=user, profile=profile))
    


@app.route('/all_stories')
def all_stories():
    return render_template("allstories.html", 
    stories=mongo.db.stories.find())


@app.route('/search')
def search():
    return render_template("index.html")


@app.route('/story/<story_to_read>/<chapter_number>')
def read(story_to_read, chapter_number):
    stories=mongo.db.stories.find()
    chapter_index = int(chapter_number) - 1
    for story in stories:
        if story_to_read == story['url']:
            this_chapter = story['chapters'][chapter_index]
            author = story['author']
            title = story['title']
            fandom = story['fandom']
            disclaimer = story['disclaimer']
            summary = story['summary']
            chapter = this_chapter
            url = story['url']
            total_chapters = len(story['chapters'])
            return render_template("story.html", story=story, story_to_read=story_to_read, title=title, author=author, fandom=fandom, chapter=chapter, chapter_number=int(chapter_number), summary=summary, disclaimer=disclaimer, total_chapters = int(total_chapters))


@app.route('/story/<story_url>/new-chapter')
def new_chapter(story_url):
    stories=mongo.db.stories.find({"url": story_url})
    for story in stories:
        if session:
            if session['username'] == story['author']:
                return render_template("addchapter.html", story=story)
            else:
                flash("You cannot edit someone else's story!")
                return redirect(url_for("index"))
        else: 
            flash("You must be signed in to edit your stories!")
            return redirect(url_for("index"))


@app.route('/story/<story_url>/new-chapter', methods=["POST"])
def add_chapter(story_url):
    stories = mongo.db.stories
    story = stories.find_one({'url': story_url})
    chapter_title = request.form['chapter_title']
    chapter_content = json.loads(request.form['editor'])
    chapter_number = request.form['chapter_number']
    chapter = {"chapter_title": chapter_title, "chapter_content": chapter_content}
    print(chapter)
    stories.find_one_and_update( {"url": story_url},
    { "$push": {
        "chapters": chapter
    }}, upsert = True
    )

    return redirect(url_for('read', story_to_read=story_url, chapter_number=chapter_number))


@app.route('/story/<story_to_read>/edit')
def edit_story(story_to_read):
    stories=mongo.db.stories.find({"url": story_to_read}) 
    for story in stories:
        if session:
            if session['username'] == story['author']:
                return render_template("editstory.html", story=story, story_to_read=story_to_read)
            else:
                flash("You cannot edit someone else's story!")
                return redirect(url_for("index"))
        else:
            flash("You must be signed in to edit your stories.")
            return redirect(url_for("index"))


@app.route('/story/<story_to_read>/edit', methods=['POST'])
def update_story(story_to_read):
    stories = mongo.db.stories
    stories.find_one_and_update( {"url": story_to_read},
    { "$set": {
        "title": request.form.get('title'),
        "summary": request.form.get('summary'),
        "author": session['username'],
        "genre": request.form.get('genre'),
        "rating": request.form.get('rating'),
        "fandom": request.form.get('fandom'),
        "disclaimer": request.form.get('disclaimer'),
    }
    })
    return redirect(url_for('profile', user = session['username']))


@app.route('/story/<story_to_read>/<chapter_number>/edit')
def edit_chapter(story_to_read, chapter_number):
    story=mongo.db.stories.find_one({"url": story_to_read}) 
    chapter_index = int(chapter_number) - 1
    if session: 
        if session['username'] == story['author']:
            chapter = story['chapters'][chapter_index]
            return render_template("editchapter.html", story_to_read=story_to_read, story=story, chapter=chapter, chapter_number=chapter_number)
        else:
            flash("You cannot edit someone else's story!")
            return redirect(url_for("index"))
    else:
        flash("You must be signed in to edit your stories!")
        return redirect(url_for("index"))


@app.route('/story/<story_to_read>/<chapter_number>/edit', methods=['POST'])
def update_chapter(story_to_read, chapter_number):
    stories = mongo.db.stories
    story = stories.find_one({'url': story_to_read})
    chapters = story['chapters']
    chapter_index = int(chapter_number) - 1
    chapters[chapter_index]['chapter_title'] = request.form['chapter_title']
    chapters[chapter_index]['chapter_content'] = json.loads(request.form['editor'])
    stories.find_one_and_update( {"url": story_to_read},
    { "$set": {
        "chapters": chapters
    }}, upsert = True
    )

    return redirect(url_for('read', story_to_read=story_to_read, chapter_number=chapter_number)) 

@app.route('/new_story')
def new_story():
    if session:
        images = ["Wings dark angel blue and white.jpg", "Wings dark angel christmas.jpg", "wings dark angel green and purple.jpg", "wings dark angel Hufflepuff.jpg", "Wings dark angel pink.jpg", "Wings dark angel stressed.jpg", "Wings dark fairy colour.jpg"]
        return render_template("newstory.html", images=images)
    else:
        flash("You must be signed in to add a story!")
        return redirect(url_for('index'))


@app.route('/new_story', methods=["POST"])
def add_story():
    if session:
        stories = mongo.db.stories
        story_url = (session['username'] + "-" + slugify(request.form.get('title'))).lower()
        stories.insert_one({
            "title": request.form.get('title'),
            "url": story_url,
            "summary": request.form.get('summary'),
            "author": session['username'],
            "genre": request.form.get('genre'),
            "rating": request.form.get('rating'),
            "fandom": request.form.get('fandom'),
            "disclaimer": request.form.get('disclaimer')
        })
        return redirect(url_for('new_chapter', story_url=story_url))
    else:
        flash("You must be signed in to add a story!")


@app.route('/story/<story_to_read>/delete')
def delete_story(story_to_read):
    story=mongo.db.stories.find_one({"url": story_to_read})
    if session: 
        if session['username'] == story['author']:
            mongo.db.stories.remove({"url": story_to_read})
            flash("Story deleted!")
            return redirect(url_for('profile', user=session['username']))
        else:
            flash("You cannot delete someone else's story!")
    else:
        flash("You must be signed in to delete stories!")
    return redirect(url_for('index'))


@app.route('/story/<story_to_read>/<chapter_number>/delete')
def delete_chapter(story_to_read, chapter_number):
    stories = mongo.db.stories
    story=mongo.db.stories.find_one({"url": story_to_read}) 
    chapter_index = int(chapter_number) - 1
    if session:
        if session['username'] == story['author']:
            chapter = story['chapters'][chapter_index]
            stories.find_one_and_update( {"url": story_to_read},
            { "$pull": {
            "chapters": chapter
            }}, upsert = True
            )
            flash("Chapter deleted!")
            return redirect(url_for("edit_story", story_to_read=story_to_read))
        else:
            flash("You cannot delete someone else's story!")
            return redirect(url_for("index"))
    else:
        flash("You must be signed in to delete chapters!")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.getenv("IP"),
            port=os.getenv("PORT"),
            debug=True)
