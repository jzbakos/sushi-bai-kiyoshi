from flask import Flask, render_template, url_for, request, redirect, jsonify, session
import os
import mysql.connector
import time

app = Flask(__name__)
app.secret_key = "super secret key"

# Default route
@app.route("/")
def index():
    return render_template("public/index.html")


# Menu route
@app.route("/menu", methods=["GET", "POST"])
def menu():
    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    if "current_order" not in session:
        session["current_order"] = []

    cursor = db.cursor()

    cursor.execute("SELECT * FROM menu_items WHERE category = 'Maki'")
    maki = cursor.fetchall()

    cursor.execute("SELECT * FROM menu_items WHERE category = 'Nigiri'")
    nigiri = cursor.fetchall()

    cursor.execute("SELECT * FROM menu_items WHERE category = 'Sashimi'")
    sashimi = cursor.fetchall()

    cursor.execute("SELECT * FROM menu_items WHERE category = 'Tempura Rolls'")
    tempura_rolls = cursor.fetchall()

    if request.method == "POST":
        menu_item_name = request.form["btn_add_to_order"]

        order_items = session["current_order"]
        order_items.append(menu_item_name)
        session["current_order"] = order_items

        message = "Added to order."
        db.close()
        return render_template(
            "public/menu.html",
            maki=maki,
            nigiri=nigiri,
            sashimi=sashimi,
            tempura_rolls=tempura_rolls,
            message=message,
        )

    db.close()

    return render_template(
        "public/menu.html",
        maki=maki,
        nigiri=nigiri,
        sashimi=sashimi,
        tempura_rolls=tempura_rolls,
    )


# Order page route
@app.route("/order", methods=["GET", "POST"])
def order():

    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    cursor = db.cursor()

    if request.method == "POST":

        if "btn_place_order" in request.form:
            if session["current_order"]:
                print("OLD SESSION: ", session["current_order"])
                new_order = []
                session["current_order"] = new_order
                print("NEW SESSION: ", session["current_order"])
                message = "Order Placed!"
                return render_template("public/index.html", message=message)
            else:
                error = "ERROR: You don't have any items in your order!"
                return render_template("public/order.html", error=error, price=0)

        order_item_name = request.form["btn_remove_from_order"]

        order = session["current_order"]

        if order_item_name in order:
            order.remove(order_item_name)

        session["current_order"] = order

    order_items = []
    order_price = 0

    if "current_order" in session:
        order = session["current_order"]

        for item in order:
            cursor.execute("SELECT * FROM menu_items WHERE name = '%s'" % item)
            menu_item = cursor.fetchall()

            order_price += float(menu_item[0][3])
            item = [menu_item[0][1], menu_item[0][3]]
            order_items.append(item)

    db.close()
    return render_template("public/order.html", order=order_items, price=order_price)


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    message = ""

    if request.method == "POST":
        print("Attemping Registration...")
        print(request.form["email"])
        print(request.form["firstName"])
        print(request.form["lastName"])
        print(request.form["phoneNumber"])
        print(request.form["password"])
        print(request.form["passwordConfirm"])
        if register_user(
            request.form["email"],
            request.form["firstName"],
            request.form["lastName"],
            request.form["phoneNumber"],
            request.form["password"],
            request.form["passwordConfirm"],
        ):

            message = "Registered Successfully!"
            print("Registered.")
            authenticate_user(request.form["email"], request.form["password"])
            return render_template("public/index.html", message=message, error=error)
        else:
            print("Error.")
            error = "User credentials are invalid. Try again."
            return render_template("public/register.html", message=error)

    return render_template("public/register.html", message=message, error=error)


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        db = mysql.connector.connect(
            user="b6a23f430401bc",
            password="4fdd2d42",
            host="us-cdbr-east-02.cleardb.com",
            database="heroku_a907c14370f5a87",
        )

        cursor = db.cursor()

        if authenticate_user(request.form["email"], request.form["password"]):

            cursor.execute(
                "SELECT * FROM users WHERE email_address = '%s'" % request.form["email"]
            )

            user = cursor.fetchall()
            name = user[0][1]

            message = "Welcome back, %s!" % name
            print("Logged In.")
            db.close()
            return render_template("public/index.html", message=message, error=error)
        else:
            db.close()
            error = "User credentials are incorrect. Try again."

    return render_template("public/login.html", error=error)


# Logout route
@app.route("/logout")
def logout():
    logout_user()
    message = "Logged out!"
    return render_template("public/index.html", message=message)


# Dashboard route(s)
@app.route("/dashboard")
def dashboard():
    error = ""
    if session.get("user"):
        if session["user"][6] == "Admin":
            return render_template("public/dashboard/overview.html")
        else:
            error = "You do not have permission to access the dashboard."
            return render_template("public/index.html", error=error)
    else:
        error = "You must be logged in to access the dashboard."
        return render_template("public/index.html", error=error)


# Dashboard: order history route
@app.route("/order_history", methods=["GET", "POST"])
def order_history():
    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    cursor = db.cursor()

    if request.method == "POST" and request.form["input_search_order"] != "":
        print("SEARCH: %s" % request.form["input_search_order"])
        cursor.execute(
            "SELECT * FROM orders WHERE order_id = '%s'"
            % request.form["input_search_order"]
        )

        myresult = cursor.fetchall()
        return render_template("public/dashboard/order_history.html", myresult=myresult)

    cursor.execute(
        "SELECT * FROM orders WHERE is_completed = 1 ORDER BY date_time_placed DESC"
    )

    myresult = cursor.fetchall()

    return render_template("public/dashboard/order_history.html", myresult=myresult)


# Dashboard: menu items route
@app.route("/menu_items")
def menu_items():
    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    cursor = db.cursor()

    cursor.execute("SELECT * FROM menu_items")

    myresult = cursor.fetchall()

    return render_template("public/dashboard/menu_items.html", myresult=myresult)


# Dashboard: order history route
@app.route("/registered_users", methods=["GET", "POST"])
def registered_users():
    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    cursor = db.cursor()

    if request.method == "POST" and request.form["input_search_user"] != "":
        print("SEARCH: %s" % request.form["input_search_user"])
        cursor.execute(
            "SELECT * FROM users WHERE user_id = '%s'"
            % request.form["input_search_user"]
        )

        myresult = cursor.fetchall()
        return render_template(
            "public/dashboard/registered_users.html", myresult=myresult
        )

    cursor.execute("SELECT * FROM users")

    myresult = cursor.fetchall()

    return render_template("public/dashboard/registered_users.html", myresult=myresult)


@app.route("/overview_num_orders")
def overview_num_orders():
    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    cursor = db.cursor()

    cursor.execute(
        "SELECT DATE(date_time_placed), COUNT(*) FROM orders WHERE DATE(date_time_placed) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) GROUP BY DATE(date_time_placed) DESC;"
    )

    myresult = cursor.fetchall()
    db.close()
    return render_template(
        "public/dashboard/overview_num_orders.html", myresult=myresult
    )


@app.route("/overview_wasted_items")
def overview_wasted_items():
    return render_template("public/dashboard/overview_wasted_items.html")


@app.route("/overview_profits")
def overview_profits():
    return render_template("public/dashboard/overview_profits.html")


# Dashboard: active orders route
@app.route("/active_orders", methods=["GET", "POST"])
def active_orders():
    db = mysql.connector.connect(
        user="b6a23f430401bc",
        password="4fdd2d42",
        host="us-cdbr-east-02.cleardb.com",
        database="heroku_a907c14370f5a87",
    )

    cursor = db.cursor()
    if request.method == "POST":
        menu_item_id = request.form["btn_complete"]
        cursor.execute(
            "UPDATE orders SET is_completed = 1 WHERE order_id = %s" % menu_item_id
        )
        date_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE orders SET date_time_completed = %s WHERE order_id = %s",
            (date_time, menu_item_id),
        )
        db.commit()

    cursor.execute(
        "SELECT * FROM orders WHERE is_completed = 0 ORDER BY date_time_placed ASC"
    )

    myresult = cursor.fetchall()
    db.close()
    return render_template("public/dashboard/active_orders.html", myresult=myresult)


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
            session["logged_in"] = True
            session["user"] = myresult[0]
            print("LOGGED IN: ", myresult[0])
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


# Register a user
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

    return True


def logout_user():
    print("LOGGED OUT: ", session["user"])
    logged_user = []
    session["user"] = logged_user
    session["logged_in"] = False


# port = os.environ["PORT"]
port = 5000
app.run(host="0.0.0.0", port=port)
