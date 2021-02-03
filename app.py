import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError



from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
app.config.from_object('config.Config')
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
    rows = db.execute("SELECT * FROM stocks WHERE user_id = :user_id", user_id=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]['cash']
    #based on https://github.com/Federico-abss/CS50-intro-course/blob/master/Python/finance/application.py
    cash_only = float(cash)
    stocks = []
    for index, row in enumerate(rows):
        stock_i = lookup(row['symbol'])
        stocks.append(list((stock_i['symbol'], stock_i['name'], row['number'], stock_i['price'], round(stock_i['price'] * row['number'], 2))))
        cash = cash_only + stocks[index][4]

    return render_template("index.html", stocks=stocks, cash=round(cash, 2), cash_only=round(cash_only, 2))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'GET':
        return render_template("buy.html")

    else:
        symbol = lookup(request.form.get("symbol"))["symbol"]
        number = int(request.form.get("number"))

        #start buy process
        if lookup(symbol):
            price = lookup(symbol)['price']
            cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]['cash']
            #cash before
            b_cash = cash
            #cash after
            a_cash = b_cash - (price * int(number))

            #if enough cash
            if a_cash >= 0:
                stock = db.execute("SELECT number FROM stocks WHERE user_id = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol)

                #update row
                if not stock:
                    db.execute("INSERT INTO stocks(user_id, symbol, number) VALUES (:user, :symbol, :number)", user=session["user_id"], symbol=symbol, number=number)

                #insert new stock row
                else:
                    number += stock[0]['number']
                    db.execute("UPDATE stocks SET number = :number WHERE user_id = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol, number=number)
                db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=a_cash, user=session["user_id"])

                #update history
                db.execute("INSERT INTO transactions(user_id, symbol, number, value) VALUES (:user, :symbol, :number, :value)", user=session["user_id"], symbol=symbol, number=number, value=round(price*float(number)))
                #redirection
                flash("Bought the stock(s)", "info")
                return redirect("/")
            #if not enough cash
            else:
                flash("You don't have enough money for this transaction", "error")
                return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    #get transactions
    j = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id = session["user_id"])

    #create table
    transactions = []
    for i in j:
        stock_i = lookup(i['symbol'])
        b_price = db.execute("SELECT value FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])[0]['value']
        a_val = stock_i["price"]


        number = db.execute("SELECT number FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])[0]['number']
        a_price = abs(a_val * float(i["number"]))
        #a_price = stock_i['price'] * abs(number)
        #if a_price != None:
            #a_val = a_price / number
        #if b_price != None:
            #b_val = b_price / number
        price_change = a_price - b_price
        value = b_price / float(i['number'])
        #value = b_val

        #create list
        #x = i['number'] * i['value']
        transactions.append(list((stock_i['symbol'], stock_i['name'], i['number'], value, b_price, stock_i['price'], price_change, i['date'])))

    #redirect
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    #forget user
    session.clear()

    error = None
    #if POST
    if request.method == "POST":

        #ensure username was input
        if not request.form.get("username"):
            flash('Please provide username!', "warning")
            return render_template('login.html')

        #ensure password was input
        elif not request.form.get("password"):
            flash('Please provide password!', "warning")
            return render_template('login.html')

        #query database
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        #verify credentials
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Invalid username and/or password!', "danger")
            return render_template('login.html')
        else:
            session["user_id"] = rows[0]["id"]

        flash('Logged in!', "success")
        #redirect
        return redirect("/")

    #if GET
    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    """Log user out"""

    flash('Logged out!', "info")
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "GET":
            return render_template("register.html")
    else:
        #inspired by https://github.com/Federico-abss/CS50-intro-course/blob/master/Python/finance/application.py
        print(request.form.get("email"))
        print(request.form.get("pass"))
        print(request.form.get("c_pass"))
        if not request.form.get("username"):
            flash("Please provide username!", "warning")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("Please provide password!", "warning")
            return render_template("register.html")
        elif request.form.get("password") != request.form.get("c_pass"):
            flash("The passwords don't match!", "warning")
            return render_template("register.html")
        #num = request.form.get("pass")
        #if len(num) < 6:
             #flash("The password isn't long enough", "warning")
             #return render_template("register.html")

        if db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username")):
            flash("The username is already taken!", "warning")
            return render_template("register.html")
        # Insert user and hash of the password into the table

        #email = request.form.get("email")
        db.execute("INSERT INTO users(username, hash, email) VALUES (:username, :hash, :email)",
            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")), email = request.form.get("email"))

        #email = request.form.get("email")
        #db.execute("INSERT INTO users(email) VALUES (:email)", email = email)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash('Welcome to Braintrooper Finance!', "info")
        return redirect("/")


@app.route("/chart", methods=["GET"])
@login_required
def chart():
    """View stocks as Chart"""
    return render_template("chart.html")

@app.route("/weather", methods=["GET"])
def weather():
    """View visitor analytics and weather of visitor location"""
    return render_template("weather.html")

@app.route("/list", methods=["GET"])
def lister():
    """View visitor analytics and weather of visitor location"""
    return render_template("list.html")

@app.route("/visitors", methods=["GET"])
def visitors():
    """View visitor analytics and weather of visitor location"""
    return render_template("visitors.html")

@app.route("/ecocalendar", methods=["GET"])
@login_required
def eccalendar():
    """View news"""
    return render_template("ecocalendar.html")

@app.route("/challenges", methods=["GET"])
@login_required
def challenges():
    """View news"""
    return render_template("challenges.html")

#@app.route("/analysis", methods=["GET", "POST"])
#@login_required
#def analysis():
#   """View stocks as Chart"""
#    if request.method == "GET":
#       return render_template("analysis.html", symbol = "")
#    else:
#        if not request.form.get("symbol"):
#            flash("Must provide symbol", "warning")
#            return render_template("analysis.html")
#        else:
#            symbol = lookup(request.form.get('symbol'))
#            if symbol:
#                return render_template("analysis.html", symbol = symbol)
#            else:
#                flash("Stock symbol doesn't exist! Please try again", "error")
#                return render_template("analysis.html", symbol = "")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html", stock = "")
    else:
        if not request.form.get("symbol"):
            flash("Must provide symbol", "warning")
            return render_template("quote.html")
        else:
            stock = lookup(request.form.get('symbol'))
            if stock:
                return render_template("quote.html", stock = stock)
            else:
                flash("Stock symbol doesn't exist! Please try again", "error")
                return render_template("quote.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        # query database with the transactions history
        j = db.execute("SELECT symbol, number FROM stocks WHERE user_id = :user_id",
                            user_id = session["user_id"])
        #create a dictionary
        stocks = {}
        for i in j:
            stocks[i['symbol']] = i['number']

        return render_template("sell.html", stocks=stocks)
    else:
        number=int(request.form.get("number"))
        symbol=request.form.get("symbol")
        price=lookup(symbol)["price"]
        value=round(price*float(number))

        #update stocks
        b_number = db.execute("SELECT number FROM stocks WHERE user_id = :user_id AND symbol = :symbol",
                          symbol=symbol, user_id=session["user_id"])[0]['number']
        a_number = b_number - number

        #halt
        if a_number < 0:
            flash("Cannot sell more stocks than you own!", "error")
            return render_template("sell.html")

        #delete row
        elif a_number == 0:
            db.execute("DELETE FROM stocks WHERE user_id = :user_id AND symbol = :symbol",
                          symbol=symbol, user_id=session["user_id"])

        #update
        else:
            db.execute("UPDATE stocks SET number = :number WHERE user_id = :user_id AND symbol = :symbol",
                          symbol=symbol, user_id=session["user_id"], number=a_number)

        #update user cash
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]['cash']
        a_cash = cash + (price * float(number))

        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                          cash=a_cash, user_id=session["user_id"])

        #update history
        db.execute("INSERT INTO transactions(user_id, symbol, number, value) VALUES (:user_id, :symbol, :number, :value)",
                user_id=session["user_id"], symbol=symbol, number=-number, value=value)

        #redirect to homepage
        flash("Sold the stock(s)!", "info")
        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)