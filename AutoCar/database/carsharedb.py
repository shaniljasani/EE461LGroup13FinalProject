# need: function that formats into a post properly
# users (list), current_cars (list), all_cars (list), duration (list) <-- corresponds to all_cars
from datetime import datetime

def add_carshare_to_collection(carshareID, users, cars, time, db):
    init_duration = []
    for car in cars:
        init_duration.append({"begin": time, "end": None})
    post = {"carshareID": carshareID,
            "users": users,
            "curr_cars": cars,
            "all_cars": cars,
            "duration": init_duration,
            "active": True}
    db.carshares.insert_one(post)


def add_user_to_carshare(carshare, usernm, db):
    carshareUsers = carshare['users']
    # add new user
    if usernm not in carshareUsers:
        carshareUsers.append(usernm)
        id, newUsers = ({"carshareID": carshare['carshareID']},
                        {
                            "$set": {
                                "users": carshareUsers
                            },
                        })
        # push to carshare collection
        db.carshares.update_one(id, newUsers)


def add_car_to_carshare(carshare, car, time, db):
    currCars = carshare['curr_cars']
    allCars = carshare['all_cars']
    duration = carshare['duration']
    # add new car
    if car['carID'] not in allCars:
        currCars.append(car['carID'])
        allCars.append(car['carID'])
        duration.append({"begin": time, "end": None})
        id, newCars = ({"carshareID": carshare['carshareID']},
                       {
                           "$set": {
                               "curr_cars": currCars,
                               "all_cars": allCars,
                               "duration": duration,
                           },
                       })
        # push to carshare collection
        db.carshares.update_one(id, newCars)
    
def readd_car_to_carshare(carshare, car, db):
    currCars = carshare['curr_cars']
    allCars = carshare['all_cars']
    duration = carshare['duration']
    carNdx = find_car_index(car['carID'], carshare)
    # add new car
    if car['carID'] in allCars:
        currCars.append(car['carID'])
        duration[carNdx]['end'] = None
        id, newCars = ({"carshareID": carshare['carshareID']},
                       {
                           "$set": {
                               "curr_cars": currCars,
                               "duration": duration,
                           },
                       })
        # push to carshare collection
        db.carshares.update_one(id, newCars)


def remove_car_from_carshare(carshare, car, time, db):
    currCars = carshare['curr_cars']
    carNdx = find_car_index(car['carID'], carshare)
    duration = carshare['duration']
    
    # remove the car from carshare
    if car['carID'] in currCars:
        carshare['curr_cars'].remove(car['carID'])
        duration[carNdx]['end'] = time
        id, newCars = ({"carshareID": carshare['carshareID']},
                       {
                           "$set": {
                               "curr_cars": currCars,
                               "duration": duration,
                           },
                       })
        # push to carshare collection
        db.carshares.update_one(id, newCars)
        return True
    return False


def get_duration_utc(carshare, car, time):
    carNdx = find_car_index(car['carID'], carshare)
    if carNdx == -1:
        return
    if car['checked_out'] is True:
        return time - carshare['duration'][carNdx]['begin']
    else:
        return carshare['duration'][carNdx]['end'], carshare['duration'][carNdx]['begin']


def close_carshare(carshare, time, db):
    currCars = carshare['curr_cars']
    for car in currCars:
        # find index of car in all_cars --> update duration
        carNdx = find_car_index(car, carshare)
        if carNdx == -1:
            return
        carshare['duration'][carNdx]['end'] = time
        # checkin car
        db.checkin_car(car)
    # make currCars empty -- carshare is closing
    currCars = []
    id, deactivate = ({"carshareID": carshare['carshareID']},
                      {
                          "$set": {
                              "active": False,
                              "curr_cars": currCars,
                              "duration": carshare['duration']
                          },
                      })
    # push to carshare collection
    db.carshares.update_one(id, deactivate)


def find_car_index(carID, carshare):
    for i, car in enumerate(carshare['all_cars']):
        if carID == car:
            return i
    return -1

def calc_days(car, carshare, time):
    allCars = carshare['all_cars']
    for cars in allCars:
        if(car == cars):
            carNdx = find_car_index(car, carshare)
            end = carshare['duration'][carNdx]['end']
            start = carshare['duration'][carNdx]['begin']
            #if car hasn't been checked in yet
            dt_end = datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")
            if(end is not None):
                dt_end = datetime.strptime(end, "%m/%d/%Y, %H:%M:%S")
            dt_start = datetime.strptime(start, "%m/%d/%Y, %H:%M:%S")
            #time delta 
            td = dt_end-dt_start
            #calc price
            days = td.days
            #one minute grace period
            if(td.seconds > 60):
                days += 1
            return days
    return None
        

