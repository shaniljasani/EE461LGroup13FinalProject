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
app.secret_key = 'secret key' # for now use just 'secret key'
app.register_blueprint(auth_bp) 
app.register_blueprint(car_bp)

# the home/main page
@app.route('/')
def index():
    return render_template("index.html")

# the dashboard page that shows cars available and carshares
@app.route('/dashboard')
def dashboard():
    db = ManageDB()
    # if the user is logged in, show their carshares as well as available cars
    if(session.get('username')):
        # get the carshares and available cars from the database and display them in the dashboard template
        return render_template("dashboard.html", carshares=db.find_user(session.get('username')).get('history'), available_cars = db.get_all_available_cars())
    # else if no one is logged in just show the available cars
    return render_template("dashboard.html", available_cars = db.get_all_available_cars())
    # close the db so we don't make copies
    db.close()
    
# the billing page
@app.route('/billing')
def file_downloads():
    if(session.get('username')):
        return render_template('billing.html')
    return render_template("login.html")

# the dataset downloads page
@app.route('/downloads')
def file_downloads():
    return render_template('downloads.html')

# the route to send car makes download to the user
@app.route('/return-carmakes')
def return_files():
    # downloads a file to the user that contains a dataset of all car makes.
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=csv')
    # TODO
    # find a different way to get the download to work, using our website's data instead of nhtsa?


    #db = ManageDB()
    #collection = db.get_cars_collection()
    #cursor = collection.find() # returns every item in the collection
    #mongoItems = list(cursor)
    #df = pd.DataFrame(mongoItems)
    #carcsv = df.to_csv(sep=',')
    #try:
        #return send_file(carcsv)#, as_attachment=True, attachment_filename='cars.csv')
    #except Exception as e:
        #return e
    #db.close()

# the route to send tesla models download to the user
@app.route('/return-teslamodels')
def redirect_tesla_download():
    # downloads a file to the user that contains tesla models
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/tesla?format=csv')

if __name__ == "__main__":
    app.run(debug=True, host="localhost")
