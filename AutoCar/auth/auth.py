import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from database.managedb import ManageDB
# import bcrypt

auth_bp = Blueprint('auth_bp', __name__)

#used for registering a user
@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form.get('inputUsername')
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        #TODO 
        #user email in db
        #encrypt password some how?
        # hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        #should the email be hashed as well?
        #what about other sensitive information like payment method?

        db = ManageDB()
        error = None
        #if user already exists error or redirect to forgot my password
        if(db.find_user(username) != None):
            error = "User already exists with that username"
        elif(db.find_user(email) != None):
            error = "User already exists with that email"
        else:
            db.add_user_to_collection(username, password)
            return redirect(url_for('auth_bp.login'))            
        
        #TODO flash error message
        db.close()
    return render_template('signup.html')

#used for logging in a user
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        username = request.form.get('inputUsername')
        password = request.form.get('inputPassword')
        #TODO
        #encrypt password some how?
        db = ManageDB()
        error = None
        #if username isnt in database
        if(db.find_user(username) == None):
            error = "User not found"
            
        #if password isnt password in db incorrect: incorrect password
        # elif not bcrypt.checkpw(password.encode(), db.find_user(email).get('password')):
        #     error = "Incorrect Password"
        elif not db.find_user(username).get('password') == password:
            error = "Incorrect Password"
        #if no error 
        if(error == None):
            session['username'] = username
            return redirect(url_for('dashboard'))
        
        db.close()
        #TODO flash error message
        # flash(error)
    return render_template('login.html')

#used to logout a user [clears cookies]
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
        