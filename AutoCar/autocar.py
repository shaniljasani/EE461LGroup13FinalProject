# EE461L Group 13
# Final Project

# TODO
# Trailing slash fix https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route
# access control

import os

from flask import Flask, render_template, g, session, send_file
from auth.auth import auth_bp
from reserve.car import car_bp
from database.managedb import ManageDB, get_db
#TODO add pandas to requirements for installing
import pandas as pd


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
    db = get_db()
    if(session.get('username')):
        return render_template("dashboard.html", carshares=db.find_user(session.get('username')).get('history'), available_cars = db.get_all_available_cars())
    return render_template("dashboard.html", available_cars = db.get_all_available_cars())

@app.route('/downloads')
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        return e

@app.route('/return-cardata')
def return_files():
    db = get_db()
    #TODO figure out how to get car data from Mongo as a csv that can be sent using send_file
    #this most likely doesn't work since I can't test it
    collection = db.get_cars_collection()
    cursor = collection.find() # returns every item in the collection
    mongoItems = list(cursor)
    df = pd.DataFrame(mongoItems)
    df.to_csv('cars.csv')

    try:
        return send_file('cars.csv', as_attachment=True, attachment_filename='cardata.csv')
    except Exception as e:
        return e

if __name__ == "__main__":
    app.run(debug=True, host="localhost")
