# EE461L Group 13
# Final Project

# TODO
# access control

import os

from flask import Flask, render_template, g, session, send_file, redirect
from auth.auth import auth_bp
from reserve.car import car_bp
from download.download import downloads_bp
from billing.billing import bill_bp
from database.managedb import ManageDB 
#TODO add pandas to requirements for installing
import pandas as pd


app = Flask(__name__, static_url_path="/static")
app.url_map.strict_slashes = False
app.secret_key = os.getenv("APP_SECRET") # secret key used for cookies in the future
app.secret_key = 'secret key' # for now use just 'secret key'
app.register_blueprint(auth_bp) 
app.register_blueprint(car_bp)
app.register_blueprint(downloads_bp)
app.register_blueprint(bill_bp)
# redirect on trainling slashes
@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

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
        ret = render_template("dashboard.html", carshares=db.find_user(session.get('username')).get('history'), available_cars = db.get_all_available_cars())
        db.close()
        return ret
    # else if no one is logged in just show the available cars
    ret = render_template("dashboard.html", available_cars = db.get_all_available_cars())
    db.close
    return ret
    # close the db so we don't make copies
    

# the dataset downloads page
@app.route('/downloads')
def file_downloads():
    return render_template('downloads.html')


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
