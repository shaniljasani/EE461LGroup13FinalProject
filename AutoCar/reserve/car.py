import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from database.managedb import ManageDB

car_bp = Blueprint('car_bp', __name__)

#reserve this car confirmation
@car_bp.route('/car', methods=('GET', 'POST'))
def car():
    # if the user is not logged in, don't allow them to reserve
    if(not session.get('username')):
            # redirect to login
            return redirect(url_for('auth_bp.login'))

    # get the car that is to be checked out
    car=request.args.get('car')
    db = ManageDB()
    # if that car doesn't exist
    if(db.find_car(car) == None):
        #some error (shouldnt ever reach here)
        return redirect(url_for('dashboard'))
    
    rend = render_template('car.html', car=db.find_car(car))
    # close the database so we don't make multiple copies
    db.close()
    return rend


#car join (join a project given the project id)
@car_bp.route('/join', methods=('GET', 'POST'))
def join():
    # make sure the user is logged in
    if(not session.get('username')):
        # if not, redirect to login
        return redirect(url_for('auth_bp.login'))

    # once someone has clicked Join
    if request.method == 'POST':
        db = ManageDB()
        # get the inputted groupID
        groupID = request.form.get('groupID')
        # if the carshare groupID doesn't exist
        if(db.find_carshare(groupID) == None):
            #TODO prompt error if no car found
            return render_template('join.html')
        #TODO should put in a request not auto join, for purpose of checkpoint it autojoins
        # if user is already in a carshare group
        if(session.get('username') in db.find_carshare(groupID)['users']):
            #TODO error that user already in group
            return render_template('join.html')
        # else if no errors, add the user to that carshare and add that to the user's history
        db.add_user_to_carshare(groupID, session.get('username'))
        # close the database so we don't make copies
        db.close()
        return redirect(url_for('dashboard'))
    return render_template('join.html')


# create a new carshare and add the selected car to new carshare
@car_bp.route('/newcs', methods=('GET', 'POST'))
def newcs():
    # make sure a user is logged in
    if(not session.get('username')):
        # otherwise redirect to login
        return redirect(url_for('auth_bp.login'))

    # open a db object
    db = ManageDB()
    #if car doesn't exist
    if db.find_car(request.args.get('car')) == None:
        #TODO car not found error
        # redirect back to home
        return render_template("index.html")

    # get the car from database
    car = db.find_car(request.args.get('car'))
    # make sure car is available
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
        # change the car's status to checked out
        # add the car to the carshare
        db.add_carshare_to_collection(g_id, [session.get('username')], [car.get('carID')])
        # add this to the user's transacation history
        db.add_carshare_to_user_history(session.get('username'), g_id)
        
        #TODO possibly redirect to another page other than the home page, like a summary page
        return redirect(url_for('car_bp.carshare', id=g_id))
    # close the database to not make copies
    db.close()
    return render_template('new_carshare.html')

#add to carshare
@car_bp.route('/addcar', methods=('GET', 'POST'))
def addcar():
    # make sure a user is logged in
    if(not session.get('username')):
        return redirect(url_for('auth_bp.login'))

    db = ManageDB()

    #if car doesn't exist
    if db.find_car(request.args.get('car')) == None:
        #TODO car not found error
        return render_template("index.html")
    # get the car from the database
    car = db.find_car(request.args.get('car'))
    # make sure the car is available
    if car.get('checked_out'):
        #TODO car got checked out already
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # make sure the car is still available
        if(car.get('checked_out')):
            return redirect(url_for('dashboard'))
        
        carshareID = request.form.get('carshare_chosen')
        #if car was already added: change car status, set car as part of curr_car and reset its end date
        if car.get('carID') in db.find_carshare(carshareID).get('all_cars'):
            db.readd_car_to_carshare(carshareID, car.get('carID'))
        else: # change the car's status to checked out # add the car to the carshare group     
            db.add_car_to_carshare(carshareID, car.get('carID'))
        db.close()
        return redirect(url_for('car_bp.carshare', id=carshareID))



    #TODO a check to see if carshare is completed or not [should not list these]
    carshares = []
    for carshareID in db.find_user(session.get('username')).get('history'):
        if db.find_carshare(carshareID).get('active') is True:
            carshares.append(carshareID)
    db.close()
    return render_template('addcar.html', carshares=carshares)


#view carshare
@car_bp.route('/carshare', methods=('GET', 'POST'))
def carshare():
    # make sure the user is logged in
    if(not session.get('username')):
        return redirect(url_for('auth_bp.login'))
    # for accessing the database
    db = ManageDB()
    # make sure the carshare exists
    if db.find_carshare(request.args.get('id')) == None:
        return redirect(url_for('dashboard'))
    # make sure the user is actually part of that carshare
    if session.get('username') not in db.find_carshare(request.args.get('id')).get('users'):
        return redirect(url_for('dashboard'))
    
    # get the carshare from the database
    carshare = db.find_carshare(request.args.get('id'))
    # list of cars that are in that carshare
    cars_list = carshare.get('all_cars')
    cars = []
    av_cars = []
    # make a list of the cars retrieved from the db
    for car in cars_list:
        c = db.find_car(car)
        if(c is not None):
            c_index = db.get_car_index(car, carshare['carshareID'])
            c['start'] = carshare['duration'][c_index]['begin']
            c['end'] = carshare['duration'][c_index]['end']
            c['days'] = db.get_car_duration(car, carshare)
            cars.append(c)
            if c['carID'] in carshare.get('curr_cars'):
                    av_cars.append(c)

    # creates buttons for checking in a car that the carshare currently has checked out
    if request.method == 'POST':
        # request to close entire cs
        if request.form.get('ID') == 'closeCS':
            for car in av_cars:
                db.remove_car_from_carshare(carshare.get('carshareID'), car.get('carID'))
            db.close_carshare(carshare.get('carshareID'))
        else: # request to check-in individual car
            for car in cars:
                if request.form.get('ID') == car.get('carID'):
                    # remove the car from the carshare & tell the database that the car is checked in
                    db.remove_car_from_carshare(carshare.get('carshareID'), car.get('carID'))

        # update the carshare now that we've removed a car from it
        carshare = db.find_carshare(request.args.get('id'))
        cars_list = carshare.get('all_cars')
        cars = []
        av_cars = []
        for car in cars_list:
            c = db.find_car(car)
            if(c is not None):
                c_index = db.get_car_index(car, carshare['carshareID'])
                c['start'] = carshare['duration'][c_index]['begin']
                c['end'] = carshare['duration'][c_index]['end']
                c['days'] = db.get_car_duration(car, carshare)
                cars.append(c)
                if c['carID'] in carshare.get('curr_cars'):
                    av_cars.append(c)
        
    
    # close the database so we don't make copies
    db.close()
    return render_template('carshare.html', cars=cars, av_cars=av_cars, carshareID=carshare['carshareID'], active=carshare['active'])
