from flask import Blueprint, redirect

downloads_bp = Blueprint('downloads_bp', __name__)

# the route to send car makes download to the user
@downloads_bp.route('/return-carmakes')
def return_carmakes():
    # downloads a file to the user that contains a dataset of all car makes.
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=csv')
    # TODO
    # [not necessary] find a different way to get the download to work, using our website's data instead of nhtsa?

    #db = ManageDB()
    #collection = db.get_cars_collection()
    #cursor = collection.find() # returns every item in the collection
    #mongoItems = list(cursor)
    #df = pd.DataFrame(mongoItems)
    #carcsv = df.to_csv(sep=',')
    #try:
        #return send_file(carcsv)#, as_attachment=True, attachment_filename='cars.csv')
    #except Exception as e:
        #return e
    #db.close()

# the route to send tesla models download to the user
@downloads_bp.route('/return-teslamodels')
def return_teslamodels():
    # downloads a file to the user that contains tesla models
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/tesla?format=csv')

# the route to send toyota models download to the user
@downloads_bp.route('/return-toyotamodels')
def return_toyotamodels():
    # downloads a file to the user that contains toyota models
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/toyota?format=csv')

# the route to send audi models download to the user
@downloads_bp.route('/return-audimodels')
def return_audimodels():
    # downloads a file to the user that contains audi models
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/audi?format=csv')

# the route to send Volvo models download to the user
@downloads_bp.route('/return-volvomodels')
def return_volvomodels():
    # downloads a file to the user that contains volvo models
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/volvo?format=csv')

# the route to send mercedes models download to the user
@downloads_bp.route('/return-mercedesmodels')
def return_mercedesmodels():
    # downloads a file to the user that contains mercedes models
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/mercedes?format=csv')

# the route to send nissan models download to the user
@downloads_bp.route('/return-nissanmodels')
def return_nissanmodels():
    # downloads a file to the user that contains nissan models
    return redirect('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/nissan?format=csv')