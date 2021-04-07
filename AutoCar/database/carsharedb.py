# need: function that formats into a post properly
# users (list), cars (list), price, duration (date checked out and checked in)


def new_carshare_post(carshareID, users, cars, price, date):
    post = {"carshareID": carshareID,
            "users": users,
            "cars": cars,
            "price": price,
            "date_checked_in": None,
            "date_checked_out": date}
    return post


def add_to_carshare_users(carshareID, newUsers):
    post = ({"carshareID": carshareID},
            {
                "$set": {
                    "users": newUsers
                },
            })
    return post


def add_to_carshare_cars(carshareID, newCars):
    post = ({"carshareID": carshareID},
            {
                "$set": {
                    "cars": newCars
                },
            })
    return post


def edit_carshare_price(carshareID, newPrice):
    post = ({"carshareID": carshareID},
            {
                "$set": {
                    "price": newPrice
                },
            })
    return post


def checkout_carshare(carshareID, checkedOut):
    post = ({"carshareID": carshareID},
            {
                "$set": {
                    "date_checked_in": checkedOut
                },
            })
    return post
