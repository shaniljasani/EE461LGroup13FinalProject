# EE461L Group 13
# Final Project

# Notes
# Trailing slash fix https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route

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

if __name__ == "__main__":
    app.run(debug=True, host="localhost")