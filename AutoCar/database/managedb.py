import pymongo
from database import userdb
from database import cardb
from database import carsharedb


class ManageDB:

    def __init__(self):
        # connects to mongoDB cluster
        client = pymongo.MongoClient(
            "mongodb+srv://amyDB:yW0lml9GAHotN5tl@teamprojectee461l.e3tgs.mongodb.net/myFirstDatabase?retryWrites"
            "=true&w=majority")
        self.client = client
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

    def get_all_users(self):
        return self.users.find({})

    def add_user_to_collection(self, usernm, password):
        # make sure this is a new username
        if self.find_user(usernm) is None:
            newUser = userdb.new_user_post(usernm, password)
            self.users.insert_one(newUser)

    # ==== CARS ====
    def edit_car_description(self, carID, newDescrip):
        car = self.find_car(carID)
        if car is not None:
            # edit the car's description
            id, descrip = cardb.update_car_description(carID, newDescrip)
            self.cars.update_one(id, descrip)

    def flip_car_status(self, carID):
        car = self.find_car(carID)
        if car is not None:
            carStat = car['checked_out']
            # flip the availability
            carStat = not carStat
            id, status = cardb.change_car_status(carID, carStat)
            # push to car collection
            self.cars.update_one(id, status)

    def set_all_cars_to_available(self):
        allCars = self.get_all_cars()
        for car in allCars:
            if car['checked_out'] is True:
                self.flip_car_status(car['carID'])

    def get_all_available_cars(self):
        availableCars = []
        allCars = self.get_all_cars()
        for car in allCars:
            if car['checked_out'] is False:
                availableCars.append(car)
        return availableCars

    def get_all_cars(self):
        return self.cars.find({})

    def add_car_to_collection(self, carID, mk, md, yr, descrip=""):
        # make sure this is a new car
        if self.find_car(carID) is None:
            newCar = cardb.new_car_post(carID, mk, md, yr, descrip)
            self.cars.insert_one(newCar)

    def add_multiple_cars_to_collection(self, cars):
        # go through all the incoming cars
        for car in cars:
            if car.get('description') is not None:
                self.add_car_to_collection(car['carID'], car['make'], car['model'], car['year'], car['description'])
            else:
                self.add_car_to_collection(car['carID'], car['make'], car['model'], car['year'])

    # ==== CARSHARES ====
    def edit_carshare_price(self, carshareID, price):
        carshare = self.find_carshare(carshareID)
        if carshare is not None:
            id, newPrice = carsharedb.edit_carshare_price(carshareID, price)
            # push to carshare collection
            self.carshares.update_one(id, newPrice)

    def checkin_carshare(self, carshareID, checkedIn):
        carshare = self.find_carshare(carshareID)
        if carshare is not None:
            id, newCheckin = carsharedb.checkin_carshare(carshareID, checkedIn)
            # push to carshare collection
            self.carshares.update_one(id, newCheckin)

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

    def get_all_carshares(self):
        return self.carshares.find({})

    def add_carshare_to_collection(self, carshareID, users, cars, price, checkedIn):
        # make sure this is a new carshare
        if self.find_carshare(carshareID) is None:
            newCarshare = carsharedb.new_carshare_post(carshareID, users, cars, price, checkedIn)
            self.carshares.insert_one(newCarshare)

    def close(self):
        self.client.close()
