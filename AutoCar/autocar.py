# EE461L Group 13
# Final Project

# TODO
# Trailing slash fix https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route
# access control

import os

from dotenv import load_dotenv
from flask import Flask, render_template

# import config env file
load_dotenv(dotenv_path="./.env")

app = Flask(__name__, static_url_path="/static")
app.secret_key = os.getenv("APP_SECRET") # secret key used for cookies in the future

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# @app.route('/car/<car_id>')
@app.route('/car')
def car():
    return render_template("car.html")

# TODO add login logic to this page
@app.route('/login')
def login():
    return render_template("login.html")

# TODO get rid of this
@app.route('/signup')
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True, host="localhost")