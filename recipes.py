import os
import csv
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
import sqlite3

app = Flask(__name__)
login_manager = LoginManager()
recipe_app_database = "recipesRB.db"


# class User(UserMixin):
#     def __init__(self, username, password):
#         self._username = # username column
#         self._password = # password column
#         self._authenticated =
#
#     @property
#     def is_active(self):
#         return True
#
#     @property
#     def get_username(self):
#         return self._username
#
#     @property
#     def is_authenticated(self):
#         return self._authenticated
#
#     def is_anonymous(self):
#         return False

# @login_manager.user_loader
# def user_loader(username):
#     return User.query.get


def create_database():
    conn = sqlite3.connect('recipesRB.db')
    conn.execute('CREATE TABLE users (name TEXT, password TEXT)')
    print("Table created successfully")
    conn.close()


def create_new_user(username, password):
    database_connection = connect_to_database()
    cursor = database_connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    database_connection.commit()
    database_connection.close()


def connect_to_database():
    return sqlite3.connect(recipe_app_database)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/<string:username>")
def profile(username):
    return render_template("profile.html", username=username)


@app.route("/user/<string:username>/upload")
@login_required
def upload(username):
    return render_template("upload.html")


@app.route("/user/<string:username>/remove")
@login_required
def remove(username):
    return render_template("remove.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html", mode="login")


@app.route("/logout")
@login_required
def logout():
    return "SIGN OUT"


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password_reentry = request.form['password2']
        if 16 >= len(username) > 4 and 20 >= len(password) > 8 and password == password_reentry:
            create_new_user(username, password)
    return render_template("login.html", mode="signup")


@app.route("/category/<string:category>")
def recipe_list(category):
    file_name = str(category) + ".csv"
    category_exists = os.path.exists(file_name)
    if category_exists:
        return render_template("category.html", category=category)
    else:
        return "404"


@app.route("/category/<string:category>/<string:recipe>")
def view_recipe(category, recipe):
    return render_template("recipe.html", category=category, recipe=recipe)



