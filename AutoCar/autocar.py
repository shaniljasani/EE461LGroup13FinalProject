# EE461L Group 13
# Final Project

# TODO
# Trailing slash fix https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route
# access control

import os

from flask import Flask, render_template, g, session, send_file, redirect
from auth.auth import auth_bp
from reserve.car import car_bp
from database.managedb import ManageDB 
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
    db = ManageDB()
    if(session.get('username')):
        return render_template("dashboard.html", carshares=db.find_user(session.get('username')).get('history'), available_cars = db.get_all_available_cars())
    return render_template("dashboard.html", available_cars = db.get_all_available_cars())
    db.close()

@app.route('/downloads')
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        return e

@app.route('/return-carmakes')
def return_files():
    db = ManageDB()
    #TODO figure out how to get car data from Mongo as a csv that can be sent using send_file
    #collection = db.get_cars_collection()
    #cursor = collection.find() # returns every item in the collection
    #mongoItems = list(cursor)
    #df = pd.DataFrame(mongoItems)
    #carcsv = df.to_csv(sep=',')

    #try:
        #return send_file(carcsv)#, as_attachment=True, attachment_filename='cars.csv')
    #except Exception as e:
        #return e

    # this gives the user a download file that contains a dataset of all car Makes.
    # Not 
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=csv')

    db.close()

@app.route('/return-teslamodels')
def redirect_tesla_download():
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/tesla?format=csv')

if __name__ == "__main__":
    app.run(debug=True, host="localhost")
