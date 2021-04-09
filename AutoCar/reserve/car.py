import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from database.managedb import ManageDB
from datetime import date

car_bp = Blueprint('car_bp', __name__)

#reserve this car confirmation
@car_bp.route('/car', methods=('GET', 'POST'))
def car():
    if(not session.get('username')):
            return redirect(url_for('auth_bp.login'))

    car=request.args.get('car')
    db = ManageDB()
    if(db.find_car(car) == None):
            #some error (shouldnt ever reach here)
        return redirect(url_for('dashboard'))
    
    rend = render_template('car.html', car=db.find_car(car))
    db.close()
    return rend


#car join {join a project based on some id}
@car_bp.route('/join', methods=('GET', 'POST'))
def join():
    if(not session.get('username')):
        return redirect(url_for('auth_bp.login'))
    if request.method == 'POST':
        db = ManageDB()
        groupID = request.form.get('groupID')
        if(db.find_carshare(groupID) == None):
            #TODO prompt error if no car found
            return render_template('join.html')
        #TODO should put in a request not auto join, for purpose of checkpoint it autojoins
        if(session.get('username') in db.find_carshare(groupID)['users']):
            #TODO error that user already in group
            return render_template('join.html')
        db.add_user_to_carshare(groupID, session.get('username'))
        db.edit_user_history(session.get('username'), groupID)
        db.close()
    return render_template('join.html')


#add to new carshare
@car_bp.route('/newcs', methods=('GET', 'POST'))
def newcs():
    if(not session.get('username')):
        return redirect(url_for('auth_bp.login'))
    db = ManageDB()

    #if car checkedout
    if db.find_car(request.args.get('car')) == None:
        #TODO car not found error
        return render_template("index.html")
    car = db.find_car(request.args.get('car'))
    if car.get('checked_out'):
        #TODO car got checked out already
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        #if car is already checked out somehow
        if(car.get('checked_out')):
            #TODO send message car just got checked out 
            return redirect(url_for('dashboard'))
        #check out the car
        
        #creates new carshare
        g_id = request.form.get('inputID')
        #if already taken do nothin TODO prompt error message
        if(db.find_carshare(g_id) != None):
            return render_template('new_carshare.html')
        db.flip_car_status(car.get('carID'))
        price = 0 #TODO software selection with price
        db.add_carshare_to_collection(g_id, [session.get('username')], [car.get('carID')], price, date.today().strftime("%b-%d-%Y"))
        db.edit_user_history(session.get('username'), g_id)
        
        #possibly redirect to another page other than the home page or a summary page
        return redirect(url_for('index'))

    db.close()
    return render_template('new_carshare.html')

#add to new carshare
@car_bp.route('/addcar', methods=('GET', 'POST'))
def addcar():
    if(not session.get('username')):
        return redirect(url_for('auth_bp.login'))
    db = ManageDB()
    #if car checkedout
    if db.find_car(request.args.get('car')) == None:
        #TODO car not found error
        return render_template("index.html")
    car = db.find_car(request.args.get('car'))
    if car.get('checked_out'):
        #TODO car got checked out already
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        if(car.get('checked_out')):
            #TODO send message car just got checked out 
            return redirect(url_for('dashboard'))
        
        #TODO update carshare price
        #check out the car
        db.flip_car_status(car.get('carID'))
        db.add_car_to_carshare(request.form.get('carshare_chosen'), car.get('carID'))

        return redirect(url_for('dashboard'))



    #TODO a check to see if carshare is completed or not [should not list these]
    rend = render_template('addcar.html', carshares=db.find_user(session.get('username')).get('history'))
    db.close()
    return rend


#view carshare
@car_bp.route('/carshare', methods=('GET', 'POST'))
def carshare():
    if(not session.get('username')):
        return redirect(url_for('auth_bp.login'))
    db = ManageDB()
    if db.find_carshare(request.args.get('id')) == None:
        return redirect(url_for('dashboard'))
    if session.get('username') not in db.find_carshare(request.args.get('id')).get('users'):
        return redirect(url_for('dashboard'))
    
    carshare = db.find_carshare(request.args.get('id'))
    cars_list = carshare.get('cars')
    cars = []
    for car in cars_list:
        c = db.find_car(car)
        if(c != None):
            cars.append(c)

    # TODO add functionality for the check-in button
    # if request.method == 'POST':
    #    for car in cars_list:
    #        if request.args.get('id') == car:
    #            db.flip_car_status(car.get('carID'))
    #            db.checkin_carshare(carshare, car.get('carID'))
    if request.method == 'POST':
        for car in cars:
            if request.form.get('ID') == car.get('carID'):
                db.remove_car_from_carshare(carshare.get('carshareID'), car.get('carID'))
                db.checkin_car(car.get('carID'))
        carshare = db.find_carshare(request.args.get('id'))
        cars_list = carshare.get('cars')
        cars = []
        for car in cars_list:
            c = db.find_car(car)
            if(c != None):
                cars.append(c)
            

    # db.flip_car_status(car.get('carID'))
    # db.checkin_carshare(db.find_carshare(request.args.get('d')), car.get('carID'))

    db.close()
    return render_template('carshare.html', cars=cars)