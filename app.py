from flask import Flask, render_template, url_for, request, redirect, jsonify
import os

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
@app.route("/register")
def register():
    return render_template("public/register.html")


# Login route
@app.route("/login")
def login():
    return render_template("public/login.html")


# port = os.environ["PORT"]
port = 5000
app.run(host="0.0.0.0", port=port)
