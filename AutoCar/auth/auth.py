import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from database.managedb import ManageDB, get_db
# import bcrypt

auth_bp = Blueprint('auth_bp', __name__)

#used for registering a user
@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        #TODO
        #encrypt password some how?
        # hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        #should the email be hashed as well?
        #what about other sensitive information like payment method?

        db = get_db()
        error = None
        #if user already exists error or redirect to forgot my password
        if(db.find_user(email) != None):
            error = "User already exists with that email"
        else:
            db.add_user_to_collection(email, password)
            return redirect(url_for('auth_bp.login'))            
        
        #TODO flash error message
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
        # elif not bcrypt.checkpw(password.encode(), db.find_user(email).get('password')):
        #     error = "Incorrect Password"

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
    return redirect(url_for('index'))
        