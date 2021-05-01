import pymongo
from datetime import datetime
from database import userdb
from database import cardb
from database import carsharedb


def get_curr_utc():
    return datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")


class ManageDB:

    def __init__(self):
        # connects to mongoDB cluster
        client = pymongo.MongoClient(
            "mongodb+srv://amyDB:yW0lml9GAHotN5tl@teamprojectee461l.e3tgs.mongodb.net/myFirstDatabase?retryWrites"
            "=true&w=majority")
        self.client = client
        # Testing Database Connection
        # self.database = client.test_database
        # Production Database Connection
        self.database = client.AutoCar

        # private attributes
        self.users = self.database.Users
        self.cars = self.database.Cars
        self.carshares = self.database.CarShares

    # accessor functions for ManageDB private attributes

    def get_users_collection(self):
        return self.users

    def get_cars_collection(self):
        return self.cars

    def get_carshares_collection(self):
        return self.carshares

    # need to find entries in each collection
    def find_user(self, usernm):
        """Returns a specified user, if not found, None"""
        return self.users.find_one({"username": usernm})

    def find_car(self, carID):
        """Returns a specified car, if not found, None"""
        return self.cars.find_one({"carID": carID})

    def find_carshare(self, carshareID):
        """Returns a specified carshare, if not found, None"""
        return self.carshares.find_one({"carshareID": carshareID})

    # ===================== USER =====================
    def get_all_users(self):
        """Returns a list of all users in the database"""
        return self.users.find({})

    def add_carshare_to_user_history(self, usernm, newCarshareID):
        """Pushes a new existing carshare id to an existing user's history, this is
        automatically called in add_user_to_carshare """
        user = self.find_user(usernm)
        # make sure this is an existing user
        if user is not None:
            userdb.edit_user_history(usernm, newCarshareID, user, self)

    def add_user_to_collection(self, usernm, password):
        """Adds a new user to the database User collection"""
        # make sure this is a new username
        if self.find_user(usernm) is None:
            userdb.add_new_user_to_collection(usernm, password, self)

    # ===================== CARS =====================
    def set_car_description(self, carID, newDescrip):
        """Changes the car's description"""

        car = self.find_car(carID)
        # make sure this is an existing car
        if car is not None:
            cardb.edit_car_description(carID, newDescrip, self)

    def set_all_cars_to_available(self):
        """Resets all cars in the Car collection to available, or checked_out = False"""
        allCars = self.get_all_cars()
        cardb.set_all_cars_to_available(allCars, self)

    # returns a list of all available cars
    def get_all_available_cars(self):
        """Returns a list of available cars in the database"""
        availableCars = []
        allCars = self.get_all_cars()
        for car in allCars:
            if car['checked_out'] is False:
                availableCars.append(car)
        return availableCars

    def get_all_cars(self):
        """Returns a list of all cars in the database"""
        return self.cars.find({})

    def checkout_car(self, carID, carshareID):
        """Sets a car's checked_out = True, sets carshareID to a valid carshare"""
        car = self.find_car(carID)
        carshare = self.find_carshare(carshareID)
        # make sure this is an existing car
        if car and carshare is not None:
            # make sure the carshare is active before adding the car
            if carshare['active'] is True:
                cardb.checkout_car(car, carshareID, self)

    def checkin_car(self, carID):
        """Sets a car's checked_out = False, sets carshareID"""
        car = self.find_car(carID)
        # make sure this is an existing car
        if car is not None:
            cardb.checkin_car(car, self)

    def add_car_to_collection(self, carID, mk, md, yr, rng, rate, descrip=""):
        """Adds a new car to the Cars collection"""
        # make sure this is a new car
        if self.find_car(carID) is None:
            cardb.add_new_car_to_collection(carID, mk, md, yr, rng, rate, descrip, self)

    def add_multiple_cars_to_collection(self, cars):
        """Adds a multiple cars to the Cars collection"""
        # go through all the incoming cars
        for car in cars:
            # check if there is a description for the car
            if car.get('description') is not None:
                self.add_car_to_collection(car['carID'], car['make'], car['model'], car['year'], car['range'], car['rate'], car['description'])
            else:
                self.add_car_to_collection(car['carID'], car['make'], car['model'], car['year'], car['range'], car['rate'])

    def get_car_rate(self, carID):
        """Gets the cars rate"""
        car = self.find_car(carID)
        # make sure this is an existing car
        if car is not None:
            return car['rate']
    # ===================== CARSHARES =====================
    def close_carshare(self, carshareID):
        """Closes a carshare and checks in all of the current cars"""
        carshare = self.find_carshare(carshareID)
        # make sure this is an existing carshare
        if carshare is not None:
            # make sure that carshare is active, otherwise do nothing
            if carshare['active'] is True:
                carsharedb.close_carshare(carshare, get_curr_utc(),  self)

    def get_all_carshares(self):
        """Returns a list of all carshares in the database"""
        return self.carshares.find({})

    def get_current_cars_in_carshare(self, carshareID):
        """Returns a list of current cars in a carshare"""
        carshare = self.find_carshare(carshareID)
        # make sure this is an existing carshare
        if carshare is not None:
            return carshare['curr_cars']

    def get_all_cars_in_carshare(self, carshareID):
        """Returns a list of all cars in a carshare"""
        carshare = self.find_carshare(carshareID)
        # make sure this is an existing carshare
        if carshare is not None:
            return carshare['all_cars']

    def get_users_in_carshare(self, carshareID):
        """Returns a list of all users in a carshare"""
        carshare = self.find_carshare(carshareID)
        # make sure this is an existing carshare
        if carshare is not None:
            return carshare['users']

    def get_car_duration_utc(self, carshareID, carID):
        """Returns a the car's hypothetical or real rent duration in UTC format"""
        car = self.find_car(carID)
        carshare = self.find_carshare(carshareID)
        # make sure this is an existing car
        if car and carshare is not None:
            carsharedb.get_duration_utc(carshare, car, get_curr_utc())

    def add_user_to_carshare(self, carshareID, usernm):
        """Add a user to a carshare and add carshare to user's history"""
        carshare = self.find_carshare(carshareID)
        # make sure this is an existing carshare and an existing user
        if carshare and self.find_user(usernm) is not None:
            carsharedb.add_user_to_carshare(carshare, usernm, self)
            # add carshare to user history as well
            self.add_carshare_to_user_history(usernm, carshareID)

    def add_car_to_carshare(self, carshareID, carID):
        """Add a new car to a carshare and set car['checked_out'] = True, inits begin duration"""
        carshare = self.find_carshare(carshareID)
        car = self.find_car(carID)
        # make sure this is an existing car and carshare
        if carshare and car is not None:
            carsharedb.add_car_to_carshare(carshare, car, get_curr_utc(), self)
            self.checkout_car(car, carshareID)

    def remove_car_from_carshare(self, carshareID, carID):
        """Remove a car from carshare and set car['checked_out'] = False, inits end duration"""
        carshare = self.find_carshare(carshareID)
        car = self.find_car(carID)
        # make sure this is an existing car and carshare
        if carshare and car is not None:
            if carsharedb.remove_car_from_carshare(carshare, car, get_curr_utc(), self) is True:
                self.checkin_car(carID)

    def add_carshare_to_collection(self, carshareID, users, cars):
        """Adds a new carshare to database Carshare Collection"""
        # make sure this is a new carshare
        if self.find_carshare(carshareID) is None:
            carsharedb.add_carshare_to_collection(carshareID, users, cars, get_curr_utc(), self)

    def get_car_duration_and_rates(self, carshareID, carID):
        """returns how long a specific car in carshare has been checked out and their rate"""
        if self.find_carshare(carshareID) is not None:
            return carsharedb.calc_days(carID, carshareID), self.get_car_rate


    def close(self):
        """Close the database connection"""
        self.client.close()
