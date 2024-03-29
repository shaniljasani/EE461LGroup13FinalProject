# **AutoCar** - A new way to (not) drive

**AutoCar** is the newest way to (not) drive! We offer high-end self-driving cars *(hardware sets)* for personal or group rent *(projects)*. 

# Table of Contents
1. [User Guide](#user-guide)
2. [Installation](#installation)
3. [Attributions](#attributions)

# User Guide

1. To start, visit the [homepage](http://autocar.pythonanywhere.com)
2. From there, you will see a navigation bar with links to the [Dashboard](http://autocar.pythonanywhere.com/dashboard), [Downloads](http://autocar.pythonanywhere.com/downloads), [Billing](http://autocar.pythonanywhere.com/billing), Login/Logout, and [Sign Up](http://autocar.pythonanywhere.com/signup)

*Without logging in, you can explore the site. To rent a car, you must be logged in*

3. To login, click [Login](http://autocar.pythonanywhere.com/login) in the navigation bar
4. Once you have logged in, the [dashboard](http://autocar.pythonanywhere.com/dashboard) tab displays all the cars available for rent *(HW Sets)*. To reserve a car *(check-out a HW Set)*, click on [Reserve Now]()
5. This will take you to the car's information page. Here, you can view details about the make, model, and year, along with an image. To the right (or below on mobile), you can reserve the car on a new reservation *(check-out to a new project)* or add to an existing rental *(check-out to an existing project)*
6. Checking out a car removes it from the list of available cars.

*To download datasets*

7. Visit the [downloads](http://autocar.pythonanywhere.com/downloads) page. 
8. Here, you will see a list of available datasets. Click on the download button and a `.csv` file will be downloaded to your computer

*To view your current rentals (projects)*

9. Scroll to the bottom of the [dashboard](http://autocar.pythonanywhere.com/dashboard) page. Here, you will see a list of all active rentals you are a part of. 
10. Click on one of the projects, and a list of cars and users within the rental will be displayed.

# Installation

### Step 1: Clone and Change Directory

```
git clone https://github.com/shaniljasani/EE461LGroup13FinalProject.git
```
```
cd EE461LGroup13FinalProject/AutoCar
```
### Step 2: Verify the correctness of the `.env` file
Use the `.env_EXAMPLE` file provided to create your `.env` file.

### Step 3: Set up a Python Virtual Environment in Directory

Run the following command to create a python virtual environment.
```
python3 -m venv venv
```
This will create a folder called `venv` in the current directory which should be the root of this project's directory. `venv` stores all the virtual environment binary files.

### Step 4: Run the Virtual Environment

The following command will start up the virtual environment
```
source venv/bin/activate
```

### Step 5: Download Dependencies
```
pip install -r requirements.txt
```

### Step 6: Start the Server
```
python autocar.py
```

# Attributions

### Team Members

- [@shaniljasani](https://github.com/shaniljasani)
- [@aimichang](https://github.com/aimichang)
- [@julianfritz](https://github.com/JulianFritz)
- [@maddisikorski](https://github.com/maddisikorski)
- [@reto0](https://github.com/Reto0)

### Resources Used 

- View presentation PDF for complete listing with purpose of resource and link
