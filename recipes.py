import os
import csv
import sys
from flask import Flask, render_template, request, redirect, url_for, Response, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/images'
app.secret_key = b'\x7f&\xd1\x8c^;\xc9\xe6\xd4g \x8bCp\x9b\x80\x9d\xb5>\x99u=0\x12'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
login_manager = LoginManager(app)
login_manager.login_view = "users"
login_manager.init_app(app)
recipe_app_database = "recipesRB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
database = SQLAlchemy(app)


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String(200))
    password = database.Column(database.String(200))


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def create_new_user(username, password):
    user = User(username=username, password=password)
    database.session.add(user)
    database.session.commit()


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", user=current_user.username)
    else:
        return render_template("index.html")


@app.route("/user/<string:username>")
def profile(username):
    if current_user.is_authenticated and current_user.username == username:
        return render_template("profile.html", username=username, my_profile=True)
    else:
        return render_template("profile.html", username=username)


@app.route("/user/<string:username>/upload", methods=['GET', 'POST'])
@login_required
def upload(username):
    if current_user.is_authenticated and current_user.username == username:
        if request.method == 'POST':
            image_file = request.files['image_upload']
            image_file.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(image_file.filename)))
            return redirect(url_for('profile', username=username))
        else:
            return render_template("upload.html", username=username)
    else:
        return redirect(url_for('profile', username=username))


@app.route("/user/<string:username>/remove")
@login_required
def remove(username):
    if current_user.is_authenticated and current_user.username == username:
        return render_template("remove.html")
    else:
        return redirect(url_for('profile', username=username))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))
    else:
        return render_template("login.html", mode="login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password_reentry = request.form['password_2']
        if 16 >= len(username) >= 8 and 20 >= len(password) > 8 and password == password_reentry:
            create_new_user(username, generate_password_hash(password))
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
