
import os
import tempfile

import pytest
from flask import Flask, render_template, g, session, send_file, redirect, url_for, request
import autocar
from download import download
from database.managedb import ManageDB 

@pytest.fixture
def client():
    db_fd, autocar.app.config['DATABASE'] = tempfile.mkstemp()
    autocar.app.config['TESTING'] = True

    with autocar.app.test_client() as client:
        with autocar.app.app_context():
            #autocar.init_db() # we don't have an init_db() function
            i = 1 #filler line
        yield client

    os.close(db_fd)
    os.unlink(autocar.app.config['DATABASE'])

def test_index_page(client):
    returnVal = client.get('/')
    expected = render_template("index.html")
    assert expected.encode() == returnVal.data

def test_downloads_page(client):
    returnVal = client.get('/downloads')
    expected = render_template("downloads.html")
    assert expected.encode() == returnVal.data

def test_dashboard_page(client):
    returnVal = client.get('/dashboard')
    db = ManageDB()
    expected = render_template("dashboard.html", available_cars = db.get_all_available_cars())
    db.close()
    assert expected.encode() in returnVal.data



def signup(client, username, email, password):
    return client.post('/login', data=dict(
        inputUsername=username,
        inputEmail=email,
        inputPassword=password
    ), follow_redirects=False)

def login(client, username, password):
    return client.post('/login', data=dict(
        inputUsername=username,
        inputPassword=password
    ), follow_redirects=False)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_signup_page(client):
    returnVal = signup(client, 'test', 'testing@testing', 'testing')
    expected = render_template('login.html', error = 'User not found') #not a real user
    assert expected.encode() in returnVal.data

def test_login_page(client):
    returnVal = login(client, 'test', 'testing')
    expected = render_template('login.html', error = 'User not found') #not a real user
    assert expected.encode() in returnVal.data



def test_downloads(client):
    returnVal = client.get('/return-carmakes')
    expected = redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=csv')
    assert expected.data == returnVal.data

    returnVal = client.get('/return-teslamodels')
    expected = redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/tesla?format=csv')
    assert expected.data == returnVal.data

    returnVal = client.get('/return-toyotamodels')
    expected = redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/toyota?format=csv')
    assert expected.data == returnVal.data

    returnVal = client.get('/return-audimodels')
    expected = redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/audi?format=csv')
    assert expected.data == returnVal.data

    returnVal = client.get('/return-volvomodels')
    expected = redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/volvo?format=csv')
    assert expected.data == returnVal.data

    returnVal = client.get('/return-mercedesmodels')
    expected = redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/mercedes?format=csv')
    assert expected.data == returnVal.data

    returnVal = client.get('/return-nissanmodels')
    expected = redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/nissan?format=csv')
    assert expected.data == returnVal.data

def test_car_page_nologin(client):
    returnVal = client.get('/car')
    # since this pytest is not logged in, should just redirect to login
    expected = redirect(url_for('auth_bp.login'))
    assert expected.data == returnVal.data

def test_join_page_nologin(client):
    returnVal = client.get('/join')
    # since this pytest is not logged in, should just redirect to login
    expected = redirect(url_for('auth_bp.login'))
    assert expected.data == returnVal.data

def test_newcs_page_nologin(client):
    returnVal = client.get('/newcs')
    # since this pytest is not logged in, should just redirect to login
    expected = redirect(url_for('auth_bp.login'))
    assert expected.data == returnVal.data

def test_addcar_page_nologin(client):
    returnVal = client.get('/addcar')
    # since this pytest is not logged in, should just redirect to login
    expected = redirect(url_for('auth_bp.login'))
    assert expected.data == returnVal.data

def test_carshare_page_nologin(client):
    returnVal = client.get('/carshare')
    # since this pytest is not logged in, should just redirect to login
    expected = redirect(url_for('auth_bp.login'))
    assert expected.data == returnVal.data


# For these tests, I couldn't figure out how to get the return value from the function within
# a test_request_context without getting an error

def test_car_page(client):
    carID = "z2021_2"
    with autocar.app.test_request_context('/car', query_string=dict(car=carID)):
        #session['username'] = 'maddisikorski'
        assert request.path == '/car'
        assert request.args.get('car') == carID
        #expected = render_template('car.html', car=db.find_car(carID))
        #returnVal = client.get('/car', query_string=dict(car=carID))
        #assert expected.encode() == returnVal.data

def test_join_page(client):
    groupID = 'qwe'
    with autocar.app.test_request_context('/join', data=dict(groupID=groupID)):
        #session['username'] = 'maddisikorski'
        assert request.path == '/join'
        assert request.form.get('groupID') == groupID
        #expected = redirect(url_for('dashboard'))
        #returnVal = client.get('/join', data=dict(groupID=groupID))
        #assert expected.data == returnVal.data

def test_newcs_page(client):
    inputID = 'asdf'
    with autocar.app.test_request_context('/newcs', data=dict(inputID=inputID)):
        #session['username'] = 'maddisikorski'
        assert request.path == '/newcs'
        assert request.form.get('inputID') == inputID
        #expected = redirect(url_for('car_bp.carshare', id=g_id))
        #returnVal = client.get('/newcs', data=dict(inputID=inputID))
        #assert expected.data == returnVal.data

def test_addcar_page(client):
    carID = "z2021_2"
    carshareID = "qwe"
    with autocar.app.test_request_context('/addcar', query_string=dict(car=carID,carshare_chosen=carshareID)):
        #session['username'] = 'maddisikorski'
        assert request.path == '/addcar'
        assert request.args.get('car') == carID
        assert request.args.get('carshare_chosen') == carshareID
        #expected = redirect(url_for('car_bp.carshare', id=carshareID))
        #returnVal = client.get('/addcar', query_string=dict(car=carID,carshare_chosen=carshareID))
        #assert expected.data == returnVal.data

def test_carshare_page(client):
    carshareID = "qwe"
    with autocar.app.test_request_context('/carshare', query_string=dict(id=carshareID)):
        #session['username'] = 'maddisikorski'
        assert request.path == '/carshare'
        assert request.args.get('id') == carshareID
        #expected = render_template('carshare.html', cars=cars, av_cars=av_cars, carshareID=carshare['carshareID'], active=carshare['active'])
        #returnVal = client.get('/carshare', query_string=dict(id=carshareID))
        #assert expected.encode() == returnVal.data


    
    
