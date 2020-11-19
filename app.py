from flask import Flask, render_template, url_for, request, redirect, jsonify
import os
import mysql.connector

app = Flask(__name__)

# Default route
@app.route("/")
def index():
    return render_template("public/index.html")


# Menu route
@app.route("/menu")
def menu():
    return render_template("public/menu.html")


# Order route
@app.route("/order")
def order():
    return render_template("public/order.html")


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        if register_user(
            request.form["email"],
            request.form["firstName"],
            request.form["lastName"],
            request.form["phoneNumber"],
            request.form["password"],
            request.form["passwordConfirm"],
        ):
            return redirect(url_for("index"))
        else:
            error = "User credentials are invalid. Try again."

    return render_template("public/register.html", error=error)


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if authenticate_user(request.form["email"], request.form["password"]):
            return redirect(url_for("index"))
        else:
            error = "User credentials are incorrect. Try again."

    return render_template("public/login.html", error=error)


# Dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template("public/dashboard.html")


# Profile route
@app.route("/profile")
def profile():
    return render_template("public/profile.html")


# Authenticate a user login attempt
def authenticate_user(email, password):
    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email_address = '%s'" % email)

    myresult = cursor.fetchall()

    # Check that passwords match
    if myresult:
        print("User found, checking password next...")
        if myresult[0][5] == password:
            print("Passwords match. Successful login!")
            db.close()
            return True
        else:
            print("Incorrect password.")
            db.close()
            return False
    else:
        print("User NOT found!")
        db.close()
        return False


def register_user(email, firstName, lastName, phoneNumber, password, passwordConfirm):
    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO users (user_id, first_name, last_Name, email_address, phone_number, password, user_type)"
        + "VALUES (NULL, %s, %s, %s, %s, %s, 'Regular');",
        (firstName, lastName, email, phoneNumber, password),
    )

    db.commit()
    db.close()


port = os.environ["PORT"]
# port = 5000
app.run(host="0.0.0.0", port=port)
