import functools
#creates a blueprint named auth
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

car_bp = Blueprint('car_bp', __name__)

#reserve this car confirmation
@car_bp.route('/reserve', methods=('GET', 'POST'))
def reserve():
    if request.method == 'POST':
        #TODO: add checked out car to user
        
        return redirect(url_for('index'))
    
    viewed_car = request.args.get('car')
    return render_template('car_reserve.html', car=viewed_car)


#car join