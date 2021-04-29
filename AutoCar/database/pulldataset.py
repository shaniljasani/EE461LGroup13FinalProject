import requests
import managedb
import random

# dataset website: https://vpic.nhtsa.dot.gov/api/
# pulling from this website to add car models to our mongo db

# for future use, if we want to use all makes available and search by makeID
# to create a huge database
getAllMakesURL = "https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json"
ret = requests.get(getAllMakesURL)
retJSON = ret.json()
finalResults = retJSON['Results']
# print out each item in finalResults
# for entry in finalResults:
#     print(entry)

# pulling only TESLA (441) makes from 2019 and later
getTesla2019URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/441/modelyear/2019?format=json"
ret = requests.get(getTesla2019URL)
retJSON = ret.json()
results2019 = retJSON['Results']

getTesla2020URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/441/modelyear/2020?format=json"
ret = requests.get(getTesla2020URL)
retJSON = ret.json()
results2020 = retJSON['Results']

getTesla2021URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/441/modelyear/2021?format=json"
ret = requests.get(getTesla2021URL)
retJSON = ret.json()
results2021 = retJSON['Results']

# debugging
# print(results2019)
# print(results2020)
# print(results2021)

# create a list of db posts for all of the car models to add to our db
allCarsFromDataSet = []
for i, car in enumerate(results2019):
    post = {"carID": "x2019_"+str(i),
            "make": car['Make_Name'],
            "model": car['Model_Name'],
            "year": "2019",
            "range": random.randrange(75) + 300,
            "rate": random.randrange(30) + 30
            }
    allCarsFromDataSet.append(post)

for i, car in enumerate(results2020):
    post = {"carID": "y2020_"+str(i),
            "make": car['Make_Name'],
            "model": car['Model_Name'],
            "year": "2020",
            "range": random.randrange(75) + 300,
            "rate": random.randrange(30) + 30
            }
    allCarsFromDataSet.append(post)

for i, car in enumerate(results2021):
    post = {"carID": "z2021_"+str(i),
            "make": car['Make_Name'],
            "model": car['Model_Name'],
            "year": "2021",
            "range": random.randrange(75) + 300,
            "rate": random.randrange(30) + 30
            }
    allCarsFromDataSet.append(post)

# push to database
db = managedb.ManageDB()
db.add_multiple_cars_to_collection(allCarsFromDataSet)
db.close()
