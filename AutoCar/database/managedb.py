import pymongo
import database.userdb
import database.cardb
import database.carsharedb
from flask import g
from database import userdb
from database import cardb
from database import carsharedb
def get_db():
        if 'db' not in g:
            g.db = ManageDB()
        return g.db

class ManageDB:
    

    def __init__(self):
        # connects to mongoDB cluster
        client = pymongo.MongoClient(
            "mongodb+srv://amyDB:yW0lml9GAHotN5tl@teamprojectee461l.e3tgs.mongodb.net/myFirstDatabase?retryWrites"
            "=true&w=majority")

        # Testing Database Connection
        self.database = client.test_database
        # Production Database Connection
        # self.database = client.AutoCar

        # private attributes
        self.users = self.database.Users
        self.cars = self.database.Cars
        self.carshares = self.database.Carshares

    # accessor functions for ManageDB private attributes

    def get_users_collection(self):
        return self.users

    def get_cars_collection(self):
        return self.cars

    def get_carshares_collection(self):
        return self.carshares

    # below functions should have the bulk of the code in respective .py files

    # need to find entries in each collection
    def find_user(self, usernm):
        return self.users.find_one({"username": usernm})

    def find_car(self, carID):
        return self.cars.find_one({"carID": carID})

    def find_carshare(self, carshareID):
        return self.carshares.find_one({"carshareID": carshareID})

    # need to edit entries in each collection
    # ==== USER ====
    def edit_user_history(self, usernm, newCarshareID):
        user = self.find_user(usernm)
        if user is not None:
            userhist = user['history']
            # add newCarshareID to userhist
            if newCarshareID not in userhist:
                userhist.append(newCarshareID)
                # split the tuple that is returned
                id, history = userdb.add_to_user_history(usernm, userhist)
                # push to user collection
                self.users.update_one(id, history)

    # need to add entries in each collection
    def add_user_to_collection(self, usernm, password):
        # make sure this is a new username
        if self.find_user(usernm) is None:
            newUser = userdb.new_user_post(usernm, password)
            self.users.insert_one(newUser)

    # ==== CARS ====
    def flip_car_status(self, carID):
        car = self.find_car(carID)
        if car is not None:
            carStat = car['checked_out']
            # flip the availability
            carStat = not carStat
            id, status = cardb.change_car_status(carID, carStat)
            # push to car collection
            self.cars.update_one(id, status)

    def add_car_to_collection(self, carID, mk, md, yr):
        # make sure this is a new car
        if self.find_car(carID) is None:
            newCar = cardb.new_car_post(carID, mk, md, yr)
            self.cars.insert_one(newCar)

    # ==== CARSHARES ====
    def edit_carshare_price(self, carshareID, price):
        carshare = self.find_carshare(carshareID)
        if carshare is not None:
            id, newPrice = carsharedb.edit_carshare_price(carshareID, price)
            # push to carshare collection
            self.carshares.update_one(id, newPrice)

    def checkout_carshare(self, carshareID, checkedOut):
        carshare = self.find_carshare(carshareID)
        if carshare is not None:
            id, newCheckout = carsharedb.edit_carshare_price(carshareID, checkedOut)
            # push to carshare collection
            self.carshares.update_one(id, newCheckout)

    def add_user_to_carshare(self, carshareID, usernm):
        carshare = self.find_carshare(carshareID)
        if carshare and self.find_user(usernm) is not None:
            carshareUsers = carshare['users']
            # add new user
            if usernm not in carshareUsers:
                carshareUsers.append(usernm)
                id, newUsers = carsharedb.add_to_carshare_users(carshareID, carshareUsers)
                # push to carshare collection
                self.carshares.update_one(id, newUsers)

    def add_car_to_carshare(self, carshareID, carID):
        carshare = self.find_carshare(carshareID)
        if carshare and self.find_car(carID) is not None:
            carshareCars = carshare['cars']
            # add new car
            if carID not in carshareCars:
                carshareCars.append(carID)
                id, newCars = carsharedb.add_to_carshare_cars(carshareID, carshareCars)
                # push to carshare collection
                self.carshares.update_one(id, newCars)

    def add_carshare_to_collection(self, carshareID, users, cars, price, checkedIn):
        # make sure this is a new carshare
        if self.find_carshare(carshareID) is None:
            newCarshare = carsharedb.new_carshare_post(carshareID, users, cars, price, checkedIn)
            self.carshares.insert_one(newCarshare)
