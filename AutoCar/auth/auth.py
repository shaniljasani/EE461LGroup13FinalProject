import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from database.managedb import ManageDB
import bcrypt

auth_bp = Blueprint('auth_bp', __name__)

#used for registering a user
@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    error = None
    if request.method == 'POST':
        username = request.form.get('inputUsername')
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        #TODO for phase 3
        # encrypt & hash password with bcrypt
        # make sure to include bcrypt install in the requirements.txt otherwise import bcrypt won't find the module
        hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        db = ManageDB()
        # if user already exists, error or redirect to forgot my password
        if(db.find_user(username) != None):
            error = "User already exists with that username"
        # if there's a user with that email
        elif(db.find_user(email) != None):
            error = "User already exists with that email"
        #if no errors, add user to database with its passowrd
        else:
            db.add_user_to_collection(username, hash_password)
            #redirect to login
            # close the ManageDB object so that we're not creating multiples
            db.close()
            return redirect(url_for('auth_bp.login'))            
        
    return render_template('signup.html', error = error)

#used for logging in a user
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        username = request.form.get('inputUsername')
        password = request.form.get('inputPassword')
        error = None
        # create db object so we can access the database
        db = ManageDB()
        # if username isnt in database
        if(db.find_user(username) == None):
            error = "User not found"
            
        #TODO for phase 3: encrypt
        else:
            try:
                hashed_pw = db.find_user(username).get('password')
                #print(type(hashed_pw))
                if not bcrypt.checkpw(password.encode(), hashed_pw):
                    error = "Incorrect Password"
            except TypeError as e:
                # I get this error: TypeError: Unicode-objects must be encoded before checking
                # when I try to login with an older previously created account
                # update: figured out that it's because older accounts were created before adding bcrypt, so those logins won't work
                error = "Account was created before password encryption was added"

        # Unencrypted version:
        # if the user's pasword does not match, throw error
        #elif not db.find_user(username).get('password') == password:
        #    error = "Incorrect Password"
        # if no error 
        if(error == None):
            # log them in by making their username the session
            session['username'] = username
            # redirect to dashboard
            return redirect(url_for('dashboard'))
        
        db.close()
    return render_template('login.html', error = error)

#used to logout a user [clears cookies]
@auth_bp.route('/logout')
def logout():
    # clear session
    session.clear()
    # redirect to homepage
    return redirect(url_for('index'))
        