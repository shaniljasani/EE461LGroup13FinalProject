import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from database.managedb import ManageDB, get_db
from datetime import date

car_bp = Blueprint('car_bp', __name__)

#reserve this car confirmation
@car_bp.route('/reserve', methods=('GET', 'POST'))
def reserve():
    if(not session.get('email')):
            return redirect(url_for('auth_bp.login'))
    if request.method == 'POST':
        car=request.args.get('car')
        db = get_db()
        #if car not in db
        if(db.find_car(car) == None):
            #some error (shouldnt ever reach here)
            return redirect(url_for('dashboard'))
        #if car is already checked out somehow
        if(db.find_car(car)['checked_out'] == True):
            #send message car just got checked out 
            return redirect(url_for('dashboard'))
        #check out the car
        db.flip_car_status(car)
        #TODO prompt to add to existing car share or create new one

        #creates new carshare
        # string for new carshare id
        g_id = session.get('email').split('@')[0] + '-' + car

        price = 0 #TODO how to get price?
        db.add_carshare_to_collection(g_id, [session.get('email')], [car], price, date.today().strftime("%b-%d-%Y"))
        
        #possibly redirect to another page other than the home page or a summary page
        return redirect(url_for('index'))
    viewed_car = request.args.get('car')
    return render_template('car_reserve.html', car=viewed_car)


#car join {join a project based on some id}
@car_bp.route('/join', methods=('GET', 'POST'))
def join():
    if(not session.get('email')):
        return redirect(url_for('auth_bp.login'))
    if request.method == 'POST':
        db = get_db()
        groupID = request.form['groupID']
        if(db.find_carshare(groupID) == None):
            #TODO prompt error if no car found
            return render_template('join.html')
        #TODO should put in a request not auto join, for purpose of checkpoint it autojoins
        if(session.get('email') in db.find_carshare(groupID)['users']):
            #TODO error that user already in group
            print(1111)
            return render_template('join.html')
        db.add_user_to_carshare(groupID, session.get('email'))
    return render_template('join.html')

#car view {sees a project and all registered users}