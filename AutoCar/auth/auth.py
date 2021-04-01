import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

auth_bp = Blueprint('auth_bp', __name__)

#used for registering a user
@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        #TODO
        #encrypt password some how?
        #if user already exists error or redirect to forgotten password
        if(True):
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
        #search db
        #if User is None: incorect email
        #if password isnt password in db incorrect: incorrect password
        #if no error 
        if(True):
            session['email'] = email
            return redirect(url_for('dashboard'))
        
        #flash error message
    return render_template('login.html')

#used to logout a user [clears cookies]
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('/'))
        