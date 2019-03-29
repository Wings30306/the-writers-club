import os
import json
from flask import Flask, app, redirect, url_for, render_template, request, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

mongo = PyMongo(app)


"""Collections"""
stories_collection = mongo.db.stories
users_collection = mongo.db.users


"""Helper functions"""


def list_by_type():
    list_by_type = {}
    ratings = []
    genres = []
    fandoms = []
    authors = []
    for story in stories_collection.find():
        rating = story['rating']
        genres_in_story = story.get('genres')
        if genres_in_story != None:
            for genre in genres_in_story:
                genre
        fandoms_in_story = story.get('fandoms')
        if fandoms_in_story != None:
            for fandom in fandoms_in_story:
                fandom
        author = story['author']
        if rating not in ratings:
            ratings.append(rating)
        if genre not in genres:
            genres.append(genre)
        if fandom not in fandoms:
            fandoms.append(fandom)
        if author not in authors:
            authors.append(author)
    list_by_type.update({"ratings": ratings, "genres": genres,
                         "fandoms": fandoms, "authors": authors})
    print(list_by_type)
    return list_by_type


def story_count():
    story_count = []
    ratings_list = list_by_type()["ratings"]
    genres_list = list_by_type()["genres"]
    fandoms_list = list_by_type()["fandoms"]
    authors_list = list_by_type()["authors"]
    for rating in ratings_list:
        count = stories_collection.count_documents({"rating": rating})
        count_rating = {"rating": rating, "total": count}
        story_count.append(count_rating)
    for genre in genres_list:
        count = stories_collection.count_documents({"genres": genre})
        count_genre = {"genre": genre, "total": count}
        story_count.append(count_genre)
    for fandom in fandoms_list:
        count = stories_collection.count_documents({"fandoms": fandom})
        count_fandom = {"fandom": fandom, "total": count}
        story_count.append(count_fandom)
    for author in authors_list:
        count = stories_collection.count_documents({"author": author})
        count_author = {"author": author, "total": count}
        story_count.append(count_author)
    return story_count


def report(item, reason_given, this_story, reported_by):
    stories_collection.find_one_and_update({"url": this_story}, {'$push': {"reports": {"item_reported": item, "reported_by": reported_by, "reason_given": reason_given}}}, upsert=True)
    return flash("Report sent to admins.")


"""Routes"""


@app.route('/')
def index():
    return render_template("index.html")


"""
User authentication with thanks to Miroslav Svec, DCD Channel lead.
Adapted from https://github.com/MiroslavSvec/DCD_lead
"""
# Sign up
@app.route('/register')
def register():
    # Check if user is not logged in already
    if 'username' in session:
        flash('You are already signed in!')
        return redirect(url_for('profile', user=session['username']))
        # Render page for user to be able to register
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def check_registration():
    form = request.form.to_dict()
    # Check if the password and password1 actualy match
    if form['user_password'] == form['user_password1']:
        # If so try to find the user in db
        user = users_collection.find_one({"user_name": form['username']})
        if user:
            flash(form['username'].title(
            ) + " already exists!  Is this you?  Please sign in instead.  Else, please choose a different username.")
            return redirect(url_for('register'))
        # If user does not exist register new user
        else:
            # Hash password
            hash_pass = generate_password_hash(form['user_password'])
            # Create new user with hashed password
            users_collection.insert_one(
                {
                    'user_name': form['username'],
                    'email': form['email'],
                    'password': hash_pass
                }
            )
            # Check if user is actualy saved
            user_in_db = users_collection.find_one(
                {"user_name": form['username']})
            if user_in_db:
                # Log user in (add to session)
                session['username'] = user_in_db['user_name']
                return redirect(url_for('profile', user=user_in_db['user_name']))
            else:
                flash("There was a problem saving your profile")
                return redirect(url_for('register'))

    else:
        flash("Passwords don't match!")
        return redirect(url_for('register'))


# Login
@app.route('/login', methods=['GET'])
def login():
        # Check if user is not logged in already
    if session.get('username') is not None:
        flash("You are logged in already!")
        return redirect(url_for('profile', user=session['username']))
    else:
        # Render the page for user to be able to log in
        return render_template("login.html")


# Check user login details from login form
@app.route('/user_auth', methods=['POST'])
def user_auth():
    form = request.form.to_dict()
    user_in_db = users_collection.find_one({"user_name": form['username']})
    # Check for user in database
    if user_in_db:
        # If passwords match (hashed / real password)
        if check_password_hash(user_in_db['password'], form['user_password']):
            # Log user in (add to session)
            session['username'] = form['username']
            session['is_admin'] = user_in_db.get('is_admin')
            print(session)

            flash("You have been successfully signed in!")
            return redirect(url_for('profile', user=user_in_db['user_name']))

        else:
            flash("Wrong password / username!")
            return redirect(url_for('login'))
    else:
        flash("You must be registered!")
        return redirect(url_for('register'))


# Log out
@app.route('/logout')
def logout():
        # Clear the session
    session.clear()
    flash('You have been logged out. We hope to see you again soon!')
    return redirect(url_for('index'))


"""
End of User AUTH
"""


@app.route('/<user>')
def profile(user):
    user_profile = users_collection.find({'user_name': user})
    user_stories = stories_collection.find({'author': user})
    return render_template("profile.html", user=user, stories=user_stories, profile=user_profile)


@app.route('/<user>/make_admin')
def make_admin(user):
    users_collection.find_one_and_update({"user_name": user}, {"$set": {"is_admin": True}})
    return redirect(url_for("profile", user=user))


@app.route('/<user>/remove_admin')
def remove_admin(user):
    users_collection.find_one_and_update({"user_name": user}, {"$set": {"is_admin": False}})
    return redirect(url_for("profile", user=user))


@app.route('/admin')
def admin_page():
    users = users_collection.find({"is_admin": True})
    if session.get("is_admin") == True:
        report_list = []
        reports = stories_collection.find({"reports": {'$gt':{'$size':0}}})
        for report in reports:
            report_list.append(report) 
        if len(report_list) > 0:
            report_list
        return render_template("adminteam.html", users=users, reports=report_list)
    return render_template("adminteam.html", users=users)


@app.route('/story/<story_to_read>/clear_report/<loop_index>')
def clear_reports(story_to_read, loop_index):
    list_index = int(loop_index) - 1
    story = stories_collection.find_one({"url": story_to_read})
    report = story['reports'][list_index]
    stories_collection.find_one_and_update({"url": story_to_read}, {'$pull': {'reports': report}})
    return redirect(url_for("admin_page"))


@app.route('/<user>/edit')
def edit_profile(user):
    if session:
        user_profile = users_collection.find({'user_name': user})
        if user == session['username']:
            return render_template("editprofile.html", user=user, profile=user_profile)
        else:
            flash("You cannot edit someone else's profile!")
            return redirect(url_for('profile', user=user, profile=profile))
    else:
        flash("You must be signed in to edit your profile.")
        return redirect(url_for("login"))


@app.route('/<user>/edit', methods=['POST'])
def update_profile(user):
    if session:
        if user == session['username']:
            users_collection.find_one_and_update({"user_name": user},
                                                 {"$set":
                                                  {
                                                      "user_name": user,
                                                      "birthday": request.form.get('birthday'),
                                                      "date_started_writing": request.form.get('date_started_writing'),
                                                      "intro": json.loads(request.form.get('editor')),
                                                      "show_birthday": request.form.get('show_birthday')
                                                  }
                                                  })
            return redirect(url_for('profile', user=user))
        else:
            flash("You cannot edit someone else's profile!")
            return redirect(url_for('profile', user=user, profile=profile))
    else:
        flash("You must be signed in to edit your profile!")
        return redirect(url_for('profile', user=user, profile=profile))


@app.route('/all_stories')
def all_stories():
    all_stories = stories_collection.find()
    return render_template("allstories.html",
                           stories=all_stories)


@app.route('/search')
def search():
    count = story_count()
    return render_template("search.html", count=count)


@app.route('/search', methods=["POST"])
def get_search_results():
    genre = request.form.get("genre")
    if genre == "No genre selected":
        genre = {'$exists': True}
    fandom = request.form.get("fandom")
    if fandom == "No fandom selected":
        fandom = {'$exists': True}
    rating = request.form.get("rating")
    if rating == "No rating selected":
        rating = {'$exists': True}
    author = request.form.get("author")
    if author == "No author selected":
        author = {'$exists': True}
    result = stories_collection.find({'$and': [{"genres": genre}, {"fandoms": fandom}, {
                                     "rating": rating}, {"author": author}]})
    return render_template("allstories.html", stories=result)


@app.route('/story/<story_to_read>/<chapter_number>')
def read(story_to_read, chapter_number):
    chapter_index = int(chapter_number) - 1
    for story in stories_collection.find({"url": story_to_read}):
        this_chapter = story['chapters'][chapter_index]
        cover_image = story.get('cover_image')
        author = story['author']
        title = story['title']
        fandoms = story['fandoms']
        disclaimer = story['disclaimer']
        summary = story['summary']
        chapter = this_chapter
        rating = story['rating']
        genres = story['genres']
        url = story['url']
        total_chapters = len(story['chapters'])
        return render_template("story.html", story=story, story_to_read=story_to_read, cover_image=cover_image, title=title, author=author, fandoms=fandoms, genres=genres, rating=rating, chapter=chapter, chapter_number=int(chapter_number), summary=summary, disclaimer=disclaimer, total_chapters=int(total_chapters))


@app.route('/story/<story_url>/new-chapter')
def new_chapter(story_url):
    for story in stories_collection.find({"url": story_url}):
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
    chapter_title = request.form['chapter_title']
    chapter_content = json.loads(request.form['editor'])
    chapter_number = request.form['chapter_number']
    chapter = {"chapter_number": chapter_number,
               "chapter_title": chapter_title,
               "chapter_content": chapter_content}
    print(chapter)
    stories_collection.find_one_and_update({"url": story_url},
                                           {"$push": {
                                               "chapters": chapter
                                           }}, upsert=True
                                           )

    return redirect(url_for('read', story_to_read=story_url, chapter_number=chapter_number))


@app.route('/story/<story_to_read>/edit')
def edit_story(story_to_read):
    for story in stories_collection.find({"url": story_to_read}):
        if session:
            if session['username'] == story['author']:
                genres = list_by_type()["genres"]
                fandoms = list_by_type()["fandoms"]
                ratings = ['Adult/NSFW', '15', '12', 'PG', 'All Ages']
                return render_template("editstory.html", story=story, story_to_read=story_to_read, genres=genres, fandoms=fandoms, ratings=ratings)
            else:
                flash("You cannot edit someone else's story!")
                return redirect(url_for("index"))
        else:
            flash("You must be signed in to edit your stories.")
            return redirect(url_for("index"))


@app.route('/story/<story_to_read>/edit', methods=['POST'])
def update_story(story_to_read):
    formatted_inputs = {}
    form_data = request.form
    for key in form_data:
        value_key = key
        key = key.split("-")
        key = key[0]
        if key in formatted_inputs:
            formatted_inputs[key].append(form_data[value_key])
        else:
            formatted_inputs[f"{key}"] = []
            formatted_inputs[key].append(form_data[value_key])
    genres = formatted_inputs.get("genre")
    if genres == None:
        genres = []
    print(genres)
    if form_data["newgenre"] is not "":
        genres.append(form_data.get("newgenre"))
    print(genres)
    fandoms = formatted_inputs.get("fandom")
    print(fandoms)
    if form_data["newfandom"] is not "":
        fandoms.append(form_data.get("newfandom"))
    print(fandoms)

    stories_collection.find_one_and_update({"url": story_to_read},
                                           {"$set": {
                                               "title": request.form.get('title'),
                                               "summary": request.form.get('summary'),
                                               "author": session['username'],
                                               "genres": genres,
                                               "rating": request.form.get('rating'),
                                               "fandoms": fandoms,
                                               "disclaimer": request.form.get('disclaimer'),
                                           }
    })
    return redirect(url_for('profile', user=session['username']))


@app.route('/story/<story_to_read>/<chapter_number>/edit')
def edit_chapter(story_to_read, chapter_number):
    story = stories_collection.find_one({"url": story_to_read})
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
    story = stories_collection.find_one({'url': story_to_read})
    chapters = story['chapters']
    chapter_index = int(chapter_number) - 1
    chapters[chapter_index]['chapter_title'] = request.form['chapter_title']
    chapters[chapter_index]['chapter_content'] = json.loads(
        request.form['editor'])
    stories_collection.find_one_and_update({"url": story_to_read},
                                           {"$set": {
                                               "chapters": chapters
                                           }}, upsert=True
                                           )

    return redirect(url_for('read', story_to_read=story_to_read, chapter_number=chapter_number))


@app.route('/new_story')
def new_story():
    if session:
        images = ["Wings dark angel blue and white.jpg", "Wings dark angel christmas.jpg", "wings dark angel green and purple.jpg",
                  "wings dark angel Hufflepuff.jpg", "Wings dark angel pink.jpg", "Wings dark angel stressed.jpg", "Wings dark fairy colour.jpg"]
        genres = list_by_type()["genres"]
        fandoms = list_by_type()["fandoms"]
        return render_template("newstory.html", images=images, genres=genres, fandoms=fandoms)
    else:
        flash("You must be signed in to add a story!")
        return redirect(url_for('index'))


@app.route('/new_story', methods=["POST"])
def add_story():
    if session:
        formatted_inputs = {}
        form_data = request.form
        for key in form_data:
            value_key = key
            key = key.split("-")
            key = key[0]
            if key in formatted_inputs:
                formatted_inputs[key].append(form_data[value_key])
            else:
                formatted_inputs[f"{key}"] = []
                formatted_inputs[key].append(form_data[value_key])
        genres = formatted_inputs.get("genre")
        if genres == None:
            genres = []
        if form_data["newgenre"] is not "":
            genres.append(form_data.get("newgenre"))
        print(genres)
        fandoms = formatted_inputs.get("fandom")
        print(fandoms)
        if fandoms == None:
            fandoms = []
        if form_data["newfandom"] is not "":
            fandoms.append(form_data.get("newfandom"))
        print(fandoms)
        story_url = (session['username'] + "-" +
                     slugify(request.form.get('title'))).lower()
        stories_collection.insert_one({
            "title": request.form.get('title').title(),
            "cover_image": request.form.get('image'),
            "url": story_url,
            "summary": request.form.get('summary'),
            "author": session['username'],
            "genres": genres,
            "rating": request.form.get('rating'),
            "fandoms": fandoms,
            "disclaimer": request.form.get('disclaimer')
        })
        return redirect(url_for('new_chapter', story_url=story_url))
    else:
        flash("You must be signed in to add a story!")


@app.route('/story/<story_to_read>/delete')
def delete_story(story_to_read):
    story = stories_collection.find_one({"url": story_to_read})
    if session:
        if session['username'] == story['author']:
            stories_collection.remove({"url": story_to_read})
            flash("Story deleted!")
            return redirect(url_for('profile', user=session['username']))
        else:
            flash("You cannot delete someone else's story!")
    else:
        flash("You must be signed in to delete stories!")
    return redirect(url_for('index'))


@app.route('/story/<story_to_read>/<chapter_number>/delete')
def delete_chapter(story_to_read, chapter_number):
    story = stories_collection.find_one({"url": story_to_read})
    chapter_index = int(chapter_number) - 1
    if session:
        if session['username'] == story['author']:
            chapter = story['chapters'][chapter_index]
            stories_collection.find_one_and_update({"url": story_to_read},
                                                   {"$pull": {
                                                       "chapters": chapter
                                                   }}, upsert=True
                                                   )
            flash("Chapter deleted!")
            return redirect(url_for("edit_story", story_to_read=story_to_read))
        else:
            flash("You cannot delete someone else's story!")
            return redirect(url_for("index"))
    else:
        flash("You must be signed in to delete chapters!")
        return redirect(url_for("index"))


@app.route('/story/<story_to_read>/<chapter_number>/feedback')
def display_fb_page(story_to_read, chapter_number):
    if session:
        stories=stories_collection.find({"url": story_to_read})
        for story in stories:
            chapter=story["chapters"][int(chapter_number) - 1]
            feedback=story.get("feedback")
        return render_template("feedback.html", story=story, chapter = chapter, feedback=feedback)
    else:
        flash("You must be signed in to post feedback.")
        return redirect(url_for('read', story_to_read=story_to_read, chapter_number=chapter_number))


@app.route('/story/<story_to_read>/<chapter_number>/feedback', methods=["POST"])
def post_feedback(story_to_read, chapter_number):
    story = story_to_read
    chapter = chapter_number
    chapter_index = int(chapter_number) - 1
    feedback = json.loads(request.form['editor'])
    posted_by = request.form['posted_by']
    feedback_post = {"fb_for_chapter": chapter, "posted_by": posted_by, "feedback_content": feedback}
    print("feedback for" + story + ", chapter " + chapter + ": " + str(feedback_post))
    stories_collection.find_one_and_update({"url": story},
                                           {"$push": {
                                               "feedback": feedback_post
                                           }}, upsert=True
                                           )
    flash("Feedback Posted")
    return redirect(url_for("display_fb_page", story_to_read=story, chapter_number=chapter))





@app.route('/story/<story_to_read>/report')
def report_story(story_to_read):
    if session:
        stories = stories_collection.find({"url": story_to_read})
        for story in stories:
            story
        return render_template('report.html', story=story)
    else:
        flash("You must be signed in to report stories.")
        return redirect(url_for('login'))


@app.route('/story/<story_to_read>/report', methods=["POST"])
def send_story_report(story_to_read):
    item = story_to_read
    reported_by = session['username']
    report_reason = request.form["reason"]
    report(item, report_reason, story_to_read, reported_by)
    return redirect(url_for("admin_page"))


if __name__ == "__main__":
    app.run(host=os.getenv("IP"),
            port=os.getenv("PORT"),
            debug=True)
