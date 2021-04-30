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

# pulling TESLA (441) makes from 2021
getTesla2021URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/441/modelyear/2021?format=json"
ret = requests.get(getTesla2021URL)
retJSON = ret.json()
retTesla2021 = retJSON['Results']

# pulling LEXUS (515) makes from 2021
getLexus2021URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/515/modelyear/2021?format=json"
ret = requests.get(getLexus2021URL)
retJSON = ret.json()
retLexus2021 = retJSON['Results']

# pulling AUDI (582) makes from 2021
getAudi2021URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/582/modelyear/2021?format=json"
ret = requests.get(getAudi2021URL)
retJSON = ret.json()
retAudi2021 = retJSON['Results']

# pulling MERCEDES (449) makes from 2021
getMer2021URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/449/modelyear/2021?format=json"
ret = requests.get(getMer2021URL)
retJSON = ret.json()
retMer2021 = retJSON['Results']

# pulling BMW (452) makes from 2021
getBMW2021URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/452/modelyear/2021?format=json"
ret = requests.get(getBMW2021URL)
retJSON = ret.json()
retBMW2021 = retJSON['Results']

# pulling Porsche (584) makes from 2021
getPor2021URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/584/modelyear/2021?format=json"
ret = requests.get(getPor2021URL)
retJSON = ret.json()
retPor2021 = retJSON['Results']

# print(retBMW2021)
# print(retMer2021)
# print(retPor2021)
# print(retAudi2021)
# print(retLexus2021)
# print(retTesla2021)

# create a list of db posts for all of the car models to add to our db
allCarsFromDataSet = []
for i, car in enumerate(retTesla2021):
    if car['Model_Name'] == 'Model 3':
        post = {"carID": "z2021_"+str(i),
                "make": car['Make_Name'],
                "model": car['Model_Name'],
                "year": "2021",
                "range": random.randrange(75) + 300,
                "rate": random.randrange(30) + 30
                }
        allCarsFromDataSet.append(post)

for i, car in enumerate(retLexus2021):
    if car['Model_Name'] == 'LS':
        post = {"carID": "z2021_"+str(i),
                "make": car['Make_Name'],
                "model": car['Model_Name'],
                "year": "2021",
                "range": random.randrange(75) + 300,
                "rate": random.randrange(30) + 10
                }
        allCarsFromDataSet.append(post)

for i, car in enumerate(retAudi2021):
    if car['Model_Name'] == 'A8':
        post = {"carID": "z2021_"+str(i),
                "make": car['Make_Name'],
                "model": car['Model_Name'],
                "year": "2021",
                "range": random.randrange(75) + 300,
                "rate": random.randrange(30) + 10
                }
        allCarsFromDataSet.append(post)

for i, car in enumerate(retMer2021):
    if car['Model_Name'] == 'S-Class':
        post = {"carID": "z2021_"+str(i),
                "make": car['Make_Name'],
                "model": car['Model_Name'],
                "year": "2021",
                "range": random.randrange(75) + 300,
                "rate": random.randrange(30) + 10
                }
        allCarsFromDataSet.append(post)

for i, car in enumerate(retBMW2021):
    if car['Model_Name'] == 'X1' or car['Model_Name'] == 'X2' or car['Model_Name'] == 'Z4':
        post = {"carID": "z2021_"+str(i),
                "make": car['Make_Name'],
                "model": car['Model_Name'],
                "year": "2021",
                "range": random.randrange(75) + 300,
                "rate": random.randrange(30) + 10
                }
        allCarsFromDataSet.append(post)

for i, car in enumerate(retPor2021):
    if car['Model_Name'] == 'Taycan' or car['Model_Name'] == 'Macan':
        post = {"carID": "z2021_"+str(i),
                "make": car['Make_Name'],
                "model": car['Model_Name'],
                "year": "2021",
                "range": random.randrange(75) + 300,
                "rate": random.randrange(30) + 10
                }
        allCarsFromDataSet.append(post)

print(allCarsFromDataSet)

# # push to database
db = managedb.ManageDB()
db.add_multiple_cars_to_collection(allCarsFromDataSet)
db.close()
