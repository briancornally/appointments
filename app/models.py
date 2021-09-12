from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app import db

@login.user_loader
def load_user(id):
    return Patient.query.get(int(id))

class Patient(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    patient_name=db.Column(db.String(64), nullable=False,unique=True)
    age=db.Column(db.Integer, nullable=False,unique=False)
    gender=db.Column(db.String(64), nullable=False,unique=False)
    password_hash=db.Column(db.String(64), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'Patient {self.patient_name}'

class Doctor(db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    doctor_name=db.Column(db.String(64), nullable=False)    

    def __repr__(self):
        return f'Doctor {self.doctor_name}'

class Appointment(db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    patient_id=db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id=db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date_time=db.Column(db.DateTime, nullable=False)
    priority=db.Column(db.String(1), nullable=True)

    def __repr__(self):
        return f'Appointment patient:{self.patient_id} doctor:{self.doctor_id} at {self.date_time}'


