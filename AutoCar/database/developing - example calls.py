from managedb import ManageDB

obj = ManageDB()

# Adding a new user to User Collection
obj.add_user_to_collection("amyc", "encrypted_password")
print(obj.find_user("amyc"))

# Adding a carID to an existing user
obj.edit_user_history("amyc", "12345")
print(obj.find_user("amyc"))

# obj.add_user_to_collection("amyc", "blah")
# print(obj.find_user("amyc"))

# Adding a new car to Car Collection
obj.add_car_to_collection("u123", "honda", "c9", "2000")
print(obj.find_car("u123"))
# Checking the flip status function
obj.flip_car_status("u123")
print(obj.find_car("u123"))

# Adding a new carshare to the Carshare Collection
obj.add_carshare_to_collection("test345", ["amyc"], ["u123"], 20.0, "2021-04-01")
print(obj.find_carshare("test345"))
# Adding an existing user to the carshare
obj.add_user_to_carshare("test345", "amyc")
print(obj.find_carshare("test345"))
obj.add_user_to_carshare("test345", "amych")
print(obj.find_carshare("test345"))
# Testing what happens if a nonexistent user is added to carshare
obj.add_user_to_carshare("test345", "amyz")
print(obj.find_carshare("test345"))
# Changing the carshare price
obj.edit_carshare_price("test345", 40.0)
print(obj.find_carshare("test345"))

# Setting all cars to available in test-database
obj.set_all_cars_to_available()
# Getting all available cars
print(obj.get_all_available_cars())
# Adding cars from Google Doc to test-database
normcars = [{"carID": "a111", "make": "Toyota", "model": "Rav4", "year": "2019"},
        {"carID": "a112", "make": "Nissan", "model": "Maxima", "year": "2020"},
        {"carID": "a113", "make": "Ford", "model": "Focus", "year": "2019"},
        {"carID": "a114", "make": "Tesla", "model": "Model S", "year": "2021"},
        {"carID": "a115", "make": "Ford", "model": "F150", "year": "2012"},
        {"carID": "a116", "make": "Honda", "model": "Accord", "year": "2016"},
        {"carID": "a117", "make": "Honda", "model": "Fit", "year": "2016"},
        {"carID": "a118", "make": "Nissan", "model": "Rogue", "year": "2016"}]
selfdrivingcars = [{"carID": "b111", "make": "Tesla", "model": "Model S", "year": "2020"},
                   {"carID": "b112", "make": "Cadillac", "model": "CT6", "year": "2020"},
                   {"carID": "b113", "make": "Nissan", "model": "Rogue", "year": "2020"},
                   {"carID": "b114", "make": "BMW", "model": "X7", "year": "2020"},
                   {"carID": "b115", "make": "Infiniti", "model": "QX50", "year": "2020"},
                   {"carID": "b116", "make": "Volvo", "model": "XC60", "year": "2020"},
                   {"carID": "b117", "make": "Mercedes-Benz", "model": "S 450", "year": "2020"},
                   {"carID": "b118", "make": "Toyota", "model": "Rav4", "year": "2021"}]
obj.add_multiple_cars_to_collection(normcars)
obj.add_multiple_cars_to_collection(selfdrivingcars)

# Adding a description to an existing car
descrip = "This is a description of the car."
obj.edit_car_description("b118", descrip)
print(obj.find_car("b118"))

# Can add a car with or without a description field
obj.add_multiple_cars_to_collection([{"carID": "c000", "make": "Toyota", "model": "Rav4", "year": "2021"}])
obj.add_multiple_cars_to_collection([{"carID": "c001", "make": "Toyota", "model": "Rav4", "year": "2021", "description": "yo this is a car!"}])

# Check in a carshare: close it, shouldn't be able to open it again/rewrite the checkin date
obj.checkin_carshare("asdf", "Apr-11-2021")
# checkout a car
obj.flip_car_status("x2019_0")
# checkin a car
obj.checkin_car("x2019_0")

# remove a car that doesn't exist from carshare
obj.remove_car_from_carshare("123455", "a113")
# remove a car from carshare
obj.remove_car_from_carshare("123455", "z2021_2")
