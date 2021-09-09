#!/usr/bin/env python3
from app import db
from app.models import *
from datetime import *
from pprint import pprint as pp

print("* recreating database ...")
db.drop_all()
db.create_all()

patient_data=[
    ("P1","25","Male"),
    ("P2","18","Female"),
    ("P3","40","Personal")
]

for (patient_name,age,gender) in patient_data:
    patient = Patient(patient_name=patient_name,age=age,gender=gender)
    patient.set_password(patient_name)
    db.session.add(patient)
db.session.commit()
print(patient.query.all())

doctor_names = ['D1','D2']
for doctor_name in doctor_names:
    doctor = Doctor(doctor_name=doctor_name)
    db.session.add(doctor)
db.session.commit()
print(doctor.query.all())

appointment_data=[
    ("D1","P1","08 03 2018 09:00:00"),
    ("D1","P1","08 04 2018 10:00:00"),
    ("D1","P2","08 03 2018 10:00:00"),
    ("D1","P1","08 04 2018 11:00:00"),
    ("D2","P1","18 03 2018 08:00:00"),
    ("D2","P1","18 04 2018 09:00:00"),
    ("D2","P3","18 03 2018 09:00:00"),
    ("D2","P3","18 04 2018 10:00:00")
]
db.session.rollback()
(doctor_name,patient_name,date_string) = appointment_data[0]
for (doctor_name,patient_name,date_string) in appointment_data:
    date_time=datetime.strptime(date_string, "%d %m %Y %H:%M:%S")
    patient=Patient.query.filter_by(patient_name=patient_name).first()
    doctor=Doctor.query.filter_by(doctor_name=doctor_name).first()
    appointment=Appointment(patient_id=patient.id,doctor_id=doctor.id,date_time=date_time)
    db.session.add(appointment)
    db.session.commit()
pp(appointment.query.all())
print("* database populated")