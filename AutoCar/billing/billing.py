from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from database.managedb import ManageDB
from datetime import date

bill_bp = Blueprint('bill_bp', __name__)

# the billing page
@bill_bp.route('/billing', methods=('GET', 'POST'))
def billing():
    # require user to be logged in
    if(not session.get('username')):
        return render_template("login.html")
    db = ManageDB()
    closed_carshares = db.find_user(session.get('username')).get('history')
    # remove active carshares as we only want to see billing for completed carshares
    for carshare in closed_carshares:
        if db.find_carshare(carshare).get('active') is True:
            closed_carshares.remove(carshare)
    # close the ManageDB object so that we're not creating multiples
    

    if request.method == 'POST':
        carshare = db.find_carshare(request.form.get('carshare_chosen'))
        # list of cars that are in that carshare
        cars_list = carshare.get('all_cars')
        cars = []
        # make a list of the cars retrieved from the db
        total = 0
        for car in cars_list:
            c = db.find_car(car)
            if(c != None):
                c_index = db.get_car_index(car, carshare['carshareID'])
                c['start'] = carshare['duration'][c_index]['begin']
                c['end'] = carshare['duration'][c_index]['end']
                c['days'] = db.get_car_duration(car, carshare)
                cars.append(c)
                total+=c['days']*c['rate']
        return render_template('billing.html', carshares=closed_carshares, cars=cars, carshareID=request.form.get('carshare_chosen'), today=date.today(), total=total)
    # close the ManageDB object so that we're not creating multiples
    db.close()
    return render_template('billing.html', carshares=closed_carshares, cars=None, carshareID=None, today=None, total = None)
    