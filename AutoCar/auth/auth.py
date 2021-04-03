import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from database.managedb import ManageDB, get_db

auth_bp = Blueprint('auth_bp', __name__)

#used for registering a user
@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        #TODO
        #encrypt password some how?
        db = get_db()
        error = None
        #if user already exists error or redirect to forgot my password
        if(db.find_user(email) != None):
            error = "User already exists with that email"
        else:
            db.add_user_to_collection(email, password)
            return redirect(url_for('auth_bp.login'))            
        
        #flash error message
    return render_template('signup.html')

#used for logging in a user
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        #TODO
        #encrypt password some how?
        db = get_db()
        error = None
        #if username/email isnt in database
        if(db.find_user(email) == None):
            error = "User not found"
        #if password isnt password in db incorrect: incorrect password
        #TODO unencrypt password
        elif(db.find_user(email).get('password') != password):
            error = "Incorrect Password"

        #if no error 
        if(error == None):
            session['email'] = email
            return redirect(url_for('dashboard'))
        

        #TODO flash error message
        # flash(error)
    return render_template('login.html')

#used to logout a user [clears cookies]
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('/'))
        