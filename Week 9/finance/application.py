import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask.helpers import get_flashed_messages
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT symbol, SUM(share) AS share, * FROM portfolio WHERE user_ID = ? GROUP BY symbol HAVING (SUM(share)) > 0", session["user_id"])
    current_cash = user_cash()

    total = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total"] = stock["price"] * int(stock["share"])
        total = total + stock["total"]

    total_cash = total + current_cash

    return render_template("index.html", stocks=stocks, current_cash=current_cash, total_cash=total_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        n_shares = request.form.get("shares")

        if not n_shares.isdigit():
            return apology("Invalid amount of shares", 400)

        if int(n_shares) < 1:
            return apology("Buy at least one", 400)

        quote = lookup(symbol)
        if quote == None:
            return apology("Stock not found", 400)

        chart_value = quote["price"] * int(n_shares)
        stock_name = quote["name"]
        stock_price = quote["price"]
        current_cash = user_cash()

        if current_cash < int(chart_value):
            return apology("Can't afford it", 400)

        update_cash = round(current_cash - chart_value)
        date = datetime.datetime.now()
        date_format = date.strftime("%d-%m-%y %H:%M:%S")

        stockid = db.execute("SELECT stock_id FROM portfolio WHERE symbol = ? AND user_id = ?", symbol, session["user_id"])

        if len(stockid) != 0:
            s_id = stockid[0]["stock_id"]
            db.execute("UPDATE portfolio SET share = share + ? WHERE user_id = ? AND stock_id = ?",
                       n_shares, session["user_id"], s_id)

        else:
            db.execute("INSERT INTO portfolio (name, symbol, price, share, user_id) VALUES (?, ?, ?, ?, ?)",
                       stock_name, symbol, stock_price, n_shares, session["user_id"])

        db.execute("INSERT INTO history (name, symbol, price, share, date, type, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   stock_name, symbol, stock_price, n_shares, date_format, 'Buy', session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, session["user_id"])

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY date DESC", session["user_id"])
    price = history[0]["price"]
    share = history[0]["share"]
    total = price * share

    return render_template("history.html", history=history, total=total)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        if request.form.get("confirmation"):
            db.execute("DELETE FROM history WHERE user_id = ?", session["user_id"])
            db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
            db.execute("DELETE FROM portfolio WHERE user_id = ?", session["user_id"])
            logout()
            flash("Account Deleted")
            return redirect("/login")
        else:
            return redirect("/")
    else:
        return render_template("delete.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if quote == None:
            return apology("Stock not found", 400)
        stock_name = quote["name"]
        stock_price = quote["price"]

        return render_template("quoted.html", stock_symbol=symbol.upper(), stock_name=stock_name, stock_price=stock_price)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
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
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    my_stocks = db.execute("SELECT stock_id, symbol, share FROM portfolio WHERE user_id = ? GROUP BY symbol", session["user_id"])

    if request.method == "POST":
        symbol = request.form.get("symbol")
        n_shares = request.form.get("shares")
        for_sale = my_stocks[0]["share"]
        stock_id = db.execute("SELECT stock_id FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        if int(n_shares) > for_sale:
            return apology("Sell what you own", 400)

        quote = lookup(symbol)
        stock_name = quote["name"]
        stock_price = quote["price"]
        value = quote["price"] * int(n_shares)
        current_cash = user_cash()
        update_cash = current_cash + value
        date = datetime.datetime.now()
        date_format = date.strftime("%d-%m-%y %H:%M:%S")

        # Delete from portfolio
        remaining = for_sale - int(n_shares)
        if remaining == 0:
            db.execute("DELETE FROM portfolio WHERE symbol = ? AND user_id = ?", symbol, session["user_id"])
        else:
            db.execute("UPDATE portfolio SET share = ? WHERE symbol = ? AND user_id = ?", remaining, symbol, session["user_id"])

        # insert into history
        db.execute("INSERT INTO history (name, symbol, price, share, date, type, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   stock_name, symbol, stock_price, n_shares, date_format, 'Sell', session["user_id"])

        # update cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, session["user_id"])

        flash("Sold!!")

        return redirect("/")
    else:
        return render_template("sell.html", my_stocks=my_stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


def user_cash():
    row = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    return row[0]["cash"]