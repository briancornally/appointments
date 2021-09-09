Hospital Appointment System
=====
This is a simple Python Flask Web App with SQLite3 database, SQLAlchemy & WTforms. 

Patient must authenticate to book appointment. Doctor appointments can be viewed without authentication. 

## Requirements
1. Python 3.6 or greater
2. Install [SQLite3](http://www.sqlite.org/download.html)
3. Recommend [dbeaver](https://dbeaver.io) to browse SQLite 

## Setup
0. Create Virtual Environment (Optional)
```
$ python3 -m venv .venv
$ source .venv/bin/activate 
$ alias python3="$(echo "$PWD/.venv/bin/python3" | sed -e 's/ /\\ /')"
$ alias pip3="$(echo "$PWD/.venv/bin/pip3" | sed -e 's/ /\\ /')"
```

1. Install flask and packages
```
$ pip3 install -r requirements.txt
```

2. Define the project
```
$ export FLASK_ENV=development
$ export FLASK_APP=app
```

## Q1: Load initial data
1. Populate the database with sample data by invoking script in the project directory
```
python populate.py
```

## Running Flask
1. Run the flask application from the project directory, running on localhost
```
$ flask run
```
2. Open the app in browser: [localhost](http://127.0.0.1:5000/)

## Q2: Get all appointments for the given doctor & date
1. Open [doctor_appts](http://127.0.0.1:5000/doctor_appts)
2. Select Doctor Name in Filter
3. Click [Filter] Button

## Q3: Patient makes an appointment by selecting doctor and date and time
1. Open [appt_schedule](http://127.0.0.1:5000/appt_schedule)
2. Enter Doctor Name, Date, Time
3. Click [Schedule] Button

## Q4: Patient cancels appointment by selecting doctor and date & time
1. Open [appt_cancel](http://127.0.0.1:5000/appt_cancel)
2. Select appointment to cancel
3. Click [Cancel] Button

## Assumptions
- This is a minimal time limited proof of concept not ready for production use

## Future work
- Test Cases
- Install Script
- Dockerize
- Improve Validation
- Prevent concurrent appointments
- Improve GUI
- Add authentication for Doctor, Admin
- ...