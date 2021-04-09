# need: function that formats into a post properly
# make, model, year, status


def new_car_post(carID, mk, md, yr, descrip):
    post = {"carID": carID,
            "make": mk,
            "model": md,
            "year": yr,
            "description": descrip,
            "checked_out": False}
    return post


def change_car_status(carID, status):
    post = ({"carID": carID},
            {
                "$set": {
                    "checked_out": status
                },
            })
    return post


def update_car_description(carID, descrip):
    post = ({"carID": carID},
            {
                "$set": {
                    "description": descrip
                },
            })
    return post
