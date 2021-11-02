import os
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# helpers.py from CS50's staff
from helpers import apology, login_required, lookup, top_ten_movies, top_ten_series, get_info, get_gravatar

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to use SQLite database
db = SQL("sqlite:///movies.db")


if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
def index():

    movies = top_ten_movies()
    shows = top_ten_series()

    if session.get("user_id") is not None:
        favorites = db.execute("SELECT imdb_id FROM favorites WHERE user_id = ?", session["user_id"])
        check = []
        for i in range(len(favorites)):
            check.append(favorites[i]["imdb_id"])

        return render_template("index.html", movies=movies, shows=shows, check=check)
    else:
        return render_template("index.html", movies=movies, shows=shows)



@app.route("/favorite", methods=["GET", "POST"])
@login_required
def favorite():
    """Save favorites"""
    if request.method == "POST":
        imdb_id = request.form.get("imdb_id")
        check = db.execute("SELECT * FROM favorites WHERE (imdb_id, user_id) = (?, ?)", imdb_id, session["user_id"])
        if len(check) == 0:
            db.execute("INSERT INTO favorites (imdb_id, user_id) VALUES (?, ?)", imdb_id, session["user_id"])

        return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        username = username.lower()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password:
            return apology("Fields can't be blank", 400)
        elif confirmation != password:
            return apology("Passwords don't match", 400)
        check = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(check) == 1:
            return apology("Username already exists", 400)
        hashed = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed)
        return redirect("/login")
    return render_template("register.html", f2="footer")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        username = request.form.get("username")
        username = username.lower()

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", f2="footer")

@app.route("/info", methods=["GET", "POST"])
def info():
    """Display information about movies and/or series"""
    # Get
    if request.method == "POST":
        imdb_id = request.form.get("imdb_id")
        ms = get_info(imdb_id)
        similars = ms["similars"]

        if session.get("user_id") is not None:
            favorites = db.execute("SELECT imdb_id FROM favorites WHERE user_id = ?", session["user_id"])
            check = []
            for i in range(len(favorites)):
                check.append(favorites[i]["imdb_id"])
            return render_template("ms_info.html", ms=ms, similars=similars, check=check)


        return render_template("ms_info.html", ms=ms, similars=similars)

@app.route("/mylist")
@login_required
def mylist():
    """List of Favorites"""
    favorites = db.execute("SELECT imdb_id FROM favorites WHERE user_id = ?", session["user_id"])
    if len(favorites) == 0:
        return apology("You don't have favorites yet!", 403)

    else:
        check = []
        for i in range(len(favorites)):
            check.append(favorites[i]["imdb_id"])

        my_list = []
        for favorite in favorites:
            my_list.append(get_info(favorite["imdb_id"]))

        return render_template("mylist.html", my_list=my_list, check=check)


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """Remove from favorites"""
    if request.method == "POST":
        imdb_id = request.form.get("imdb_id")
        db.execute("DELETE FROM favorites WHERE imdb_id = ? AND user_id = ?", imdb_id, session["user_id"])
        return redirect("/")


@app.route("/profile")
@login_required
def profile():
    """User Profile"""
    g = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    email = g[0]["username"]

    favorites = db.execute("SELECT * FROM favorites WHERE user_id = ?", session["user_id"])
    number = len(favorites)

    gravatar = get_gravatar(email)
    if not gravatar:
        return render_template("profile.html", number=number, f2="footer")
    gravatar = gravatar[0]


    return render_template("profile.html", gravatar=gravatar, number=number, f1="footer")

@app.route("/logout")
def logout():
    """"Logout"""

    # Forget any user_id
    session.clear()

    # Redirect user to index
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    """Lookup movie or series"""
    if request.method == "POST":
        title = request.form.get("search")
        results = lookup(title)
        if results == None:
            return apology("Not found", 400)
        if session.get("user_id") is not None:
            favorites = db.execute("SELECT imdb_id FROM favorites WHERE user_id = ?", session["user_id"])
            check = []
            for i in range(len(favorites)):
                check.append(favorites[i]["imdb_id"])
            return render_template("search.html", results=results, check=check)
        return render_template("search.html", results=results)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Delete user"""
    if request.method == "POST":
        if request.form.get("confirmation"):
            db.execute("DELETE FROM favorites WHERE user_id = ?", session["user_id"])
            db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
            logout()
            return redirect("/")
        else:
            return redirect("/")
    else:
        return render_template("delete.html")