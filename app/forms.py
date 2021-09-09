from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField, SelectField, widgets
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_login import current_user
from app.models import *
import datetime

class LoginForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Register')

class DoctorChoiceIterable(object):
    def __iter__(self):
        doctors=Doctor.query.all()
        choices=[(doctor.id,doctor.doctor_name) for doctor in doctors] 
        for choice in choices:
            yield choice

class AppointmentScheduleForm(FlaskForm):
    doctor=SelectField('Doctor',coerce=int,choices=DoctorChoiceIterable())
    date=DateField('Date', format="%m/%d/%Y")
    hour=SelectField('Time',coerce=int,choices=[(i,i) for i in range(8,16)])
    submit=SubmitField('Schedule') 

class MeetingChoiceIterable(object):
    def __iter__(self):
        patient=current_user
        choices=[(appointment.id,f'{Doctor.query.filter_by(id=appointment.doctor_id).first() } at {appointment.date_time}') for appointment in Appointment.query.filter_by(patient_id=patient.id)] 
        for choice in choices:
            yield choice

class AppointmentCancelForm(FlaskForm):
    choices=MeetingChoiceIterable()
    if choices:
        id=SelectField('Choose appointment to cancel',coerce=int,choices=choices) 
        submit=SubmitField('Cancel')    

class FilterForm(FlaskForm):
    choices = DoctorChoiceIterable()
    if choices:
        doctor = SelectField("Doctor", coerce=int, choices=choices)
        # doctor = IntegerField("Doctor")
        submit = SubmitField("Filter")
