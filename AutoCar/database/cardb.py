# need: function that formats into a post properly
# make, model, year, status, rate, range (mileage)

# create a new car post for the db and define the fields that it has
def add_new_car_to_collection(carID, mk, md, yr, rng, rate, descrip, db):

    post = {"carID": carID,
            "make": mk,
            "model": md,
            "year": yr,
            "range": rng,
            "rate": rate,
            "description": descrip,
            "carshareID": None,
            "checked_out": False}
    db.cars.insert_one(post)


def checkin_car(car, db):
    id, status = ({"carID": car['carID']},
                  {
                      "$set": {
                          "checked_out": False,
                          "carshareID": None,
                      },
                  })
    db.cars.update_one(id, status)


def checkout_car(car, carshareID, db):
    id, status = ({"carID": car['carID']},
                  {
                      "$set": {
                          "checked_out": True,
                          "carshareID": carshareID,
                      },
                  })
    db.cars.update_one(id, status)


def set_all_cars_to_available(cars, db):
    for car in cars:
        if car['checked_out'] is True:
            id, status = ({"carID": car['carID']},
                          {
                              "$set": {
                                  "checked_out": False,
                                  "carshareID": None,
                              },
                          })
            db.cars.update_one(id, status)


def edit_car_description(carID, descrip, db):
    id, descrip = ({"carID": carID},
                   {
                        "$set": {
                            "description": descrip
                        },
                   })
    db.cars.update_one(id, descrip)
