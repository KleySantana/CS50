import os
import requests
import urllib.parse

from libgravatar import Gravatar
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def top_ten_movies():
    api_key = os.environ.get("API_KEY")
    try:
        url = f"https://imdb-api.com/API/Top250Movies/{api_key}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        movies = response.json()
        y = movies["items"]
        x = y[:10]
        for i in range(len(x)):
            rate = x[i]["imDbRating"]
            if len(rate) == 0:
                x[i]["imDbRating"] = "Unrated"

        #print(f"{x}")
        return x


    except requests.RequestException:
       return None


def top_ten_series():
    api_key = os.environ.get("API_KEY")
    try:
        url = f"https://imdb-api.com/en/API/Top250TVs/{api_key}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        series = response.json()
        y = series["items"]
        x = y[:10]
        for i in range(len(x)):
            rate = x[i]["imDbRating"]
            if len(rate) == 0:
                x[i]["imDbRating"] = "Unrated"
            
        return x

    except requests.RequestException:
        return None

def lookup(search):
    """Look up info about title."""

    # Contact API
    api_key = os.environ.get("API_KEY")
    try:
        # Need several API calls. Get them at https://imdb-api.com/api
        # Search into all titles, movie or series
        url = f"https://imdb-api.com/en/API/SearchTitle/{api_key}/{search}/"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    # Parse response
    try:
        result = response.json()
        x = result["results"]
        return x

    except (KeyError, TypeError, ValueError):
        return None


def get_gravatar(email):
    x = Gravatar(email)
    try:
        url = f"{x.get_profile()}.json"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        profile = response.json()
        return profile["entry"]

    except requests.RequestException:
        return None

def get_info(result_id):
    try:
        api_key = os.environ.get("API_KEY")

        url = f"https://imdb-api.com/en/API/Title/{api_key}/{result_id}/"
        response = requests.get(url)
        response.raise_for_status()

         #Get trailer. Need id.
        url1 = f"https://imdb-api.com/API/Trailer/{api_key}/{result_id}"
        response_1 = requests.get(url1)
        response_1.raise_for_status()

        url2 = f"https://imdb-api.com/API/Posters/{api_key}/{result_id}"
        response2 = requests.get(url2)
        response2.raise_for_status()

    except requests.RequestException:
        return None


    try:
        result = response.json()

        result1 = response_1.json()
        trailer = result1["link"]

        result2 = response2.json()
        images = result2["backdrops"]
        image = images[0]["link"]

        result["trailer"] = trailer
        result["image"] = image


        return result
    except (KeyError, TypeError, ValueError):
        return None
