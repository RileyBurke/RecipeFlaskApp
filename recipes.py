import os
import csv
import random

from flask import Flask, render_template, request, redirect, url_for, flash
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
login_manager.init_app(app)\

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


def remove_from_file(recipe_to_remove: list):
    all_recipes = load_recipe_file()
    with open("recipes.csv", "w", newline="") as recipe_file:
        writer = csv.writer(recipe_file)
        for recipe in all_recipes:
            if recipe != recipe_to_remove:
                writer.writerow(recipe)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@login_manager.unauthorized_handler
def unauthorized_user():
    return redirect(url_for('index'))


def create_new_user(username, password):
    user = User(username=username, password=password)
    database.session.add(user)
    database.session.commit()


def get_random_recipe():
    all_recipes = load_recipe_file()
    recipe = all_recipes[random.randint(0, len(all_recipes) - 1)]
    return recipe


@app.route("/")
def index():
    error = request.args.get('error')
    random_recipe = request.args.get('random_recipe')
    if random_recipe == "Random Recipe":
        recipe = get_random_recipe()
        ingredients = recipe[3].replace('\'', '').replace('[', '').replace(']', '').split(',')
        return render_template("recipe.html", category=recipe[1], recipe=recipe[0], recipe_info=recipe,
                               ingredients=ingredients)
    if current_user.is_authenticated:
        return render_template("index.html", logged_user=current_user.username, error=error)
    else:
        return render_template("index.html", error=error)


@app.route("/user/<string:username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        all_recipes = load_recipe_file()
        recipes_by_user = []
        for recipe in all_recipes:
            if recipe[5] == username.lower():
                recipes_by_user.append(recipe)
        if current_user.is_authenticated and current_user.username == username.lower():
            return render_template("profile.html", username=username.lower(), my_profile=True,
                                   recipes_list=recipes_by_user)
        else:
            return render_template("profile.html", username=username.lower(), recipes_list=recipes_by_user)
    else:
        flash("User not found.")
        return redirect(url_for('index', error=True))


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
                if recipes[0].lower() == name.lower():
                    recipe_name_in_use = True
            category = request.form['recipe_category']
            serving_size = request.form['serving_size']
            ingredients = request.form['ingredients'].split("\n")
            instructions = request.form['instructions']
            file_extension = image_file.filename.split(".")[-1]
            if name == "" or category == "" or serving_size == "" or len(ingredients) == 0 or instructions == "" \
                    or image_file.filename == "":
                flash("All information must be filled.")
                return render_template("upload.html", username=username.lower(), error=True)
            elif file_extension not in ALLOWED_FILE_EXTENSIONS:
                flash("Image must be a png, jpg, or bmp file.")
                return render_template("upload.html", username=username.lower(), error=True)
            elif recipe_name_in_use:
                flash("Recipe name is already in use!")
                return render_template("upload.html", username=username.lower(), error=True)
            else:
                unique_id = uuid.uuid4()  # Used to prevent duplicate image names.
                image_file.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(str(unique_id) +
                                                                                        image_file.filename)))
                recipe = [name, category, serving_size, ingredients, instructions, current_user.username,
                          str(unique_id) + image_file.filename]
                add_recipe_file(recipe)
                return redirect(url_for('profile', username=username.lower()))
        else:
            return render_template("upload.html", username=username.lower())
    else:
        return redirect(url_for('profile', username=username.lower()))


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
            return redirect(url_for('profile', username=username.lower()))
        else:
            user_recipes = []
            for recipe in all_recipes:
                if recipe[5] == current_user.username:
                    user_recipes.append(recipe)
            return render_template("remove.html", user_recipes=user_recipes, username=username)
    else:
        return redirect(url_for('profile', username=username.lower()))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form['username'].lower()
        password = request.form['password_1']
        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login', error=True))
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
        username = request.form['username'].lower()
        password = request.form['password_1']
        password_reentry = request.form['password_2']
        existing_user = User.query.filter_by(username=username).first()
        if 16 >= len(username) >= 8 and 20 >= len(password) >= 8 and password == password_reentry \
                and existing_user is None:
            create_new_user(username, generate_password_hash(password))
            flash("User successfully created.")
            return redirect(url_for('login'))
        else:
            if 16 < len(username) or len(username) < 8:
                flash("Username must be 8 to 16 characters.")
            if 20 < len(password) or len(password) < 8:
                flash("Password must be 8 to 20 characters.")
            if password != password_reentry:
                flash("Passwords must match.")
            if existing_user is not None:
                flash("Username already exists.")
            return render_template("login.html", mode="signup", error=True)
    else:
        return render_template("login.html", mode="signup")


@app.route("/category/<string:category>/")
def recipe_list(category):
    all_recipes = load_recipe_file()
    recipes_in_category = []
    for recipe in all_recipes:
        if recipe[1].lower() == category.lower():
            recipes_in_category.append(recipe)
    if not recipes_in_category:
        flash("Category does not exist.")
        return redirect(url_for('index', error=True))
    else:
        return render_template("category.html", category=category, recipes_list=recipes_in_category)


@app.route("/category/<string:category>/<string:recipe>/")
def view_recipe(category, recipe):
    all_recipes = load_recipe_file()
    for recipes in all_recipes:
        if recipes[0].lower() == recipe.lower():
            ingredients = recipes[3].replace('\'', '').replace('[', '').replace(']', '').split(',')
            return render_template("recipe.html", category=category, recipe=recipe, recipe_info=recipes,
                                   ingredients=ingredients)
    else:
        flash("Could not find specified recipe.")
        return redirect(url_for('index', error=True))


@app.errorhandler(404)
def page_not_found(e):
    flash("404 invalid URL.")
    return redirect(url_for('index', error=True))
