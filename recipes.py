import os
import csv
from flask import Flask, render_template, request, redirect, url_for
import flask_login
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/<string:username>")
def profile(username):
    return render_template("profile.html")


@app.route("/user/<string:username>/upload")
def upload(username):
    return render_template("upload.html")


@app.route("/user/<string:username>/remove")
def remove(username):
    return render_template("remove.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    return "SIGN OUT"


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/<string:category>")
def recipe_list(category):
    file_name = str(category) + ".csv"
    category_exists = os.path.exists(file_name)
    if category_exists:
        return render_template("category.html", category=category)
    else:
        return "404"


@app.route("/<string:category>/<string:recipe>")
def view_recipe(category, recipe):
    return render_template("recipe.html", category=category, recipe=recipe)
