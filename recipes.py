import os
import csv
import sys

from flask import Flask, render_template, request, redirect, url_for, Response, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/images'
app.secret_key = b'\x7f&\xd1\x8c^;\xc9\xe6\xd4g \x8bCp\x9b\x80\x9d\xb5>\x99u=0\x12'
app.debug = True
login_manager = LoginManager(app)
login_manager.login_view = "users"
recipe_app_database = "recipesRB.db"


class User(UserMixin):
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._authenticated = False

    @property
    def is_active(self):
        return self.is_active

    @property
    def get_username(self):
        return self._username

    @property
    def is_authenticated(self):
        return self._authenticated

    def is_anonymous(self):
        return False


@login_manager.user_loader
def load_user(username):
    database_connection = connect_to_database()
    cursor = database_connection.cursor()
    cursor.execute("SELECT * FROM login WHERE username = (?)", username)
    user = cursor.fetchone()
    if user is None:
        return None
    else:
        return User(user[0], user[1])


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


def delete_user(user_to_delete, password_to_delete):
    database_connection = connect_to_database()
    cursor = database_connection.cursor()
    cursor.execute("DELETE FROM users WHERE (username, password) = (?, ?)", (user_to_delete, password_to_delete))
    database_connection.commit()
    database_connection.close()


def get_users():
    database_connection = connect_to_database()
    cursor = database_connection.cursor()
    cursor.execute("SELECT username, password FROM users")
    users = cursor.fetchall()
    database_connection.close()
    return users


def connect_to_database():
    return sqlite3.connect(recipe_app_database)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/<string:username>")
def profile(username):
    return render_template("profile.html", username=username)


@app.route("/user/<string:username>/upload", methods=['GET', 'POST'])
@login_required
def upload(username):
    if request.method == 'POST':
        image_file = request.files['image_upload']
        image_file.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(image_file.filename)))
    else:
        return render_template("upload.html")


@app.route("/user/<string:username>/remove")
@login_required
def remove(username):
    return render_template("remove.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        valid_user = False

        for user in users:
            if user[0] == username and user[1] == password:
                valid_user = True
        if valid_user:
            pass
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))
    else:
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
        password_reentry = request.form['password_2']
        users = get_users()
        username_taken = False
        print(users, file=sys.stderr)
        for user in users:
            if user[0] == username:
                username_taken = True
        if 16 >= len(username) >= 8 and 20 >= len(password) > 8 and password == password_reentry and not username_taken:
            create_new_user(username, password)
            flash("User successfully created.")
            return redirect(url_for('login'))
        else:
            return render_template("login.html", mode="signup", error="Username already exists.")
    else:
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
