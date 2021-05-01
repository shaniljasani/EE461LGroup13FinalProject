# **AutoCar** - A new way to (not) drive

**AutoCar** is the newest way to (not) drive! We offer high-end self-driving cars *(hardware sets)* for personal or group rent *(projects)*. 

# Table of Contents
1. [User Guide](#user-guide)
2. [Installation](#installation)
3. [Attributions](#attributions)

# User Guide


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

- [Bootstrap Landing Page](https://www.freecodecamp.org/news/learn-bootstrap-4-in-30-minute-by-building-a-landing-page-website-guide-for-beginners-f64e03833f33/)
- [Photo by Unsplash](https://unsplash.com/@introspectivedsgn?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
