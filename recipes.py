import os
import csv
import sys
from flask import Flask, render_template, request, redirect, url_for, Response, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import uuid

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
ALLOWED_FILE_EXTENSIONS = {"bmp", "png", "jpg", "jpeg"}


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String(200))
    password = database.Column(database.String(200))


def load_recipe_file():
    recipes = []
    with open("recipes.csv", newline="") as recipe_file:
        reader = csv.reader(recipe_file)
        for row in reader:
            recipes.append(row)
    return recipes


def add_recipe_file(recipe: list):
    with open("recipes.csv", "a", newline="") as recipe_file:
        writer = csv.writer(recipe_file)
        writer.writerow(recipe)


def remove_from_file(recipe_to_remove:list):
    all_recipes = load_recipe_file()
    with open("recipes.csv", "w", newline="") as recipe_file:
        writer = csv.writer(recipe_file)
        for recipe in all_recipes:
            if recipe != recipe_to_remove:
                writer.writerow(recipe)

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
        return render_template("index.html", logged_user=current_user.username)
    else:
        return render_template("index.html")


@app.route("/user/<string:username>")
def profile(username):
    all_recipes = load_recipe_file()
    recipes_by_user = []
    for recipe in all_recipes:
        if recipe[5] == username:
            recipes_by_user.append(recipe)
    if current_user.is_authenticated and current_user.username == username:
        return render_template("profile.html", username=username, my_profile=True, recipes_list=recipes_by_user)
    else:
        return render_template("profile.html", username=username, recipes_list=recipes_by_user)


@app.route("/user/<string:username>/upload", methods=['GET', 'POST'])
@login_required
def upload(username):
    if current_user.is_authenticated and current_user.username == username:
        if request.method == 'POST':
            recipe_name_in_use = False
            image_file = request.files['image_upload']
            name = request.form['recipe_name']
            all_recipes = load_recipe_file()
            for recipes in all_recipes:
                if recipes[0] == name:
                    recipe_name_in_use = True
            category = request.form['recipe_category']
            serving_size = request.form['serving_size']
            ingredients = request.form['ingredients']
            instructions = request.form['instructions']
            file_extension = image_file.filename.split(".")[-1]
            if name == "" or category == "" or serving_size == "" or ingredients == "" or instructions == "" \
                    or image_file.filename == "":
                flash("All information must be filled.")
                return render_template("upload.html", username=username)
            elif file_extension not in ALLOWED_FILE_EXTENSIONS:
                flash("Image must be a png, jpg, or bmp file.")
                return render_template("upload.html", username=username)
            elif recipe_name_in_use:
                flash("Recipe name is already in use!")
                return render_template("upload.html", username=username)
            else:
                unique_id = uuid.uuid4()  # Used to prevent duplicate image names.
                image_file.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(str(unique_id) +
                                                                                        image_file.filename)))
                recipe = [name, category, serving_size, ingredients, instructions, current_user.username,
                          str(unique_id) + image_file.filename]
                add_recipe_file(recipe)
                return redirect(url_for('profile', username=username))
        else:
            return render_template("upload.html", username=username)
    else:
        return redirect(url_for('profile', username=username))


@app.route("/user/<string:username>/remove", methods=['GET', 'POST'])
@login_required
def remove(username):
    if current_user.is_authenticated and current_user.username == username:
        all_recipes = load_recipe_file()
        if request.method == 'POST':
            recipes_to_remove = request.form.getlist('recipe_select')
            for recipe_to_remove in recipes_to_remove:
                for recipe in all_recipes:
                    if recipe[0] == recipe_to_remove:
                        remove_from_file(recipe)
                        os.remove(os.path.join(app.config['UPLOAD_PATH'], recipe[6]))
            return redirect(url_for('profile', username=username))
        else:
            user_recipes = []
            for recipe in all_recipes:
                if recipe[5] == current_user.username:
                    user_recipes.append(recipe)
                return render_template("remove.html", user_recipes=user_recipes, username=username)
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
    all_recipes = load_recipe_file()
    recipes_in_category = []
    for recipe in all_recipes:
        if recipe[1] == category:
            recipes_in_category.append(recipe)
    if not recipes_in_category:
        return "No recipes uploaded in this category!"
    else:
        return render_template("category.html", category=category, recipes_list=recipes_in_category)



@app.route("/category/<string:category>/<string:recipe>")
def view_recipe(category, recipe):
    all_recipes = load_recipe_file()
    for recipes in all_recipes:
        if recipes[0] == recipe:
            return render_template("recipe.html", category=category, recipe=recipe, recipe_info=recipes)
    else:
        return "Recipe doesn't exist."
