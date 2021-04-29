# need: function that formats into a post properly
# users (list), current_cars (list), all_cars (list), duration (list) <-- corresponds to all_cars
import managedb


def add_carshare_to_collection(carshareID, users, cars, db):
    init_duration = []
    for car in cars:
        init_duration.append({"begin": managedb.get_curr_utc(), "end": None})
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


def add_car_to_carshare(carshare, car, db):
    currCars = carshare['curr_cars']
    allCars = carshare['all_cars']
    duration = carshare['duration']
    # add new car
    if car['carID'] not in allCars:
        currCars.append(car['carID'])
        allCars.append(car['carID'])
        duration.append({"begin": managedb.get_curr_utc(), "end": None})
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


def remove_car_from_carshare(carshare, car, db):
    currCars = carshare['curr_cars']
    carNdx = find_car_index(car['carID'], carshare['all_cars'])
    duration = carshare['duration']
    # remove the car from carshare
    if car['carID'] in currCars:
        currCars.remove(car['carID'])
        duration[carNdx]['end'] = managedb.get_curr_utc()
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


def get_duration_utc(carshare, car):
    carNdx = find_car_index(car['carID'], carshare['all_cars'])
    if carNdx == -1:
        return
    if car['checked_out'] is True:
        return managedb.get_curr_utc() - carshare['duration'][carNdx]['begin']
    else:
        return carshare['duration'][carNdx]['end'] - carshare['duration'][carNdx]['begin']


def close_carshare(carshare, db):
    currCars = carshare['curr_cars']
    for car in currCars:
        # find index of car in all_cars --> update duration
        carNdx = find_car_index(car, carshare['all_cars'])
        if carNdx == -1:
            return
        carshare['duration'][carNdx]['end'] = managedb.get_curr_utc()
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


def find_car_index(carID, all_cars):
    for i, car in enumerate(all_cars):
        if carID == car:
            return i
    return -1

