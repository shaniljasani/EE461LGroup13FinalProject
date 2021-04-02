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
