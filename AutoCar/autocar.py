# EE461L Group 13
# Final Project

# TODO
# Trailing slash fix https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route
# access control

import os

from dotenv import load_dotenv
from flask import Flask, render_template
from auth.auth import auth_bp
from reserve.car import car_bp

# import config env file
load_dotenv(dotenv_path="./.env")

app = Flask(__name__, static_url_path="/static")
app.secret_key = os.getenv("APP_SECRET") # secret key used for cookies in the future
app.secret_key = 'secret key'
app.register_blueprint(auth_bp)
app.register_blueprint(car_bp)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True, host="localhost")