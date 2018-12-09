import os
from flask import Flask, app, redirect, url_for, render_template, request, flash

app = Flask(__name__)


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


@app.route('/search')
def search():
    return render_template("index.html")


@app.route('/<title>')
def read(title):
    return render_template("index.html")


@app.route('/new_story')
def new_story():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host=os.getenv("IP"),
            port=os.getenv("PORT"),
            debug=True)
