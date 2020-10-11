from flask import Flask, render_template, url_for, request, redirect, jsonify
import os

app = Flask(__name__)


# Default route
@app.route("/")
def index():
    return render_template("public/index.html")


# port = os.environ["PORT"]
port = 5000
app.run(host="0.0.0.0", port=port)
