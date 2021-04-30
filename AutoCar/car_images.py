from google_images_download import google_images_download 
#pip install git+https://github.com/Joeclinton1/google-images-download.git
# creating object
response = google_images_download.googleimagesdownload() 
from PIL import Image
from database.managedb import ManageDB
import os
from glob import glob
#generates a folder of all the cars this can only be run once per "download" folder. Do need to delete before rerunning.
def import_car_images():
    db = ManageDB()
    arguments = {"keywords": "",
                 "limit":1,
                 "print_urls":True,
                 "size": "medium",
                 "format": "jpg"
                }   
    for car in db.get_all_cars():
        search = car.get('make') + " " + car.get('model') + " " + car.get('year')
        arguments["keywords"] = search
        paths = response.download(arguments)
        print(paths)
    #renames folders to car name and renames img to 0.jpg
    subfolders = [ f.path for f in os.scandir("downloads") if f.is_dir() ]
    for folder in subfolders:
        for file in [ x.path for x in os.scandir(folder)]:
            if(file == folder+"\\"+"0.jpg"):
                os.remove(folder+"\\"+"0.jpg")
                continue
            os.rename(file, folder+"\\"+"0.jpg")
        os.rename(folder, folder.replace(" ",""))
            
    
import_car_images()