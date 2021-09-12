from flask import render_template, flash, redirect, request, url_for
from werkzeug.urls import url_parse
from app import app
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from app import db
from datetime import *
import sqlite3 

@app.route('/')
@app.route('/index')
def index():
    appointments = []
    if current_user.is_authenticated:
        patient=current_user
        for appt in Appointment.query.filter_by(patient_id=patient.id).order_by("date_time").all():
            item = {
                "patient_name": Patient.query.filter_by(id=appt.patient_id).first().patient_name,
                "doctor_name": Doctor.query.filter_by(id=appt.doctor_id).first().doctor_name,
                "date_time": appt.date_time
            }
            appointments.append(item)
    return render_template('index.html', appointments=appointments)

def get_appointments(doctor_id=None):
    appointments = []
    for appt in Appointment.query.filter_by(doctor_id=doctor_id).order_by("date_time").all():
        item = {
            "patient_name": Patient.query.filter_by(id=appt.patient_id).first().patient_name,
            "doctor_name": Doctor.query.filter_by(id=appt.doctor_id).first().doctor_name,
            "date_time": appt.date_time
        }
        appointments.append(item)
    return appointments

@app.route('/doctor_appts', methods=['GET', 'POST'])
def doctor_appts():
    form = FilterForm()
    doctor_id=1
    if form.validate_on_submit():
        doctor_id=form.doctor.data
        appointments=get_appointments(doctor_id=doctor_id)
        # return redirect(url_for('doctor_appts'))
    else:
        appointments=get_appointments(doctor_id=doctor_id)
    return render_template('doctor_appts.html', appointments=appointments, form=form)

@app.route('/patient_login', methods=['GET', 'POST'])
def patient_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(patient_name=form.patient_name.data).first()
        if patient is None or not patient.check_password(form.password.data):
            flash('Invalid Patient Name or password')
            return redirect(url_for('patient_login'))
        login_user(patient, remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page=url_for('index')
        return redirect(next_page)
    return render_template('patient_login.html', title='Sign In', form=form)

@app.route('/patient_logout')
def patient_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/patient_register', methods=['GET','POST'])
def patient_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        patient_name=form.patient_name.data
        age=form.age.data
        try:
            int(age)
        except:
            flash(f"'{age}' is an invalid age. Please retry")
            return redirect(url_for('patient_register'))
    
        gender=form.gender.data
        patient=Patient(patient_name=patient_name,age=age,gender=gender)
        alreadyRegistered = Patient.query.filter_by(patient_name=patient_name).first()
        if alreadyRegistered:
            flash(f"Patient:{patient_name} is already registered. Please proceed to login or contact admin for password reset.")
        else:
            patient.set_password(form.password.data)
            db.session.add(patient)
            db.session.commit()
            flash(f"Patient:{patient_name} registration successful. Please proceed to login :)")
        return redirect(url_for('patient_login'))
    return render_template('patient_register.html',title='Register',form=form)
 
@app.route('/appt_schedule',methods=['GET','POST'])
@login_required
def appt_schedule():
    form=AppointmentScheduleForm()
    if form.validate_on_submit():
        patient=current_user
        doctor_id=form.doctor.data
        doctor=Doctor.query.filter_by(id=doctor_id).first()
        date_time=datetime.combine(form.date.data,time(hour=form.hour.data))
        priority=form.priority.data
        if priority not in ['H','L']:
            flash(f"Priority must be 'H' or 'L'. Please retry")
            return redirect(url_for('appt_schedule'))
        if Appointment.query.filter_by(date_time=date_time).filter_by(doctor_id=doctor_id).first():
            flash(f"Existing appointment on {date_time} with {doctor}. Please retry")
            return redirect(url_for('appt_schedule'))
        else:
            appointment=Appointment(patient_id=patient.id,doctor_id=doctor_id,date_time=date_time)
            db.session.add(appointment)
            db.session.commit()
            flash(f"Appointment scheduled on {date_time} with {doctor}")
            return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('appt_schedule.html',title='Appointment',form=form)


@app.route('/appt_cancel',methods=['GET','POST'])
@login_required
def appt_cancel():
    if not current_user.is_authenticated:
        flash('Please Log in to cancel appointment')
        return redirect(url_for('login')) 

    patient=current_user
    if not Appointment.query.filter_by(patient_id=patient.id).count():
        flash(f"Dear Patient {current_user.patient_name}. You have no appointments to cancel.")
        return redirect(url_for('index'))
    
    form=AppointmentCancelForm()
    if form.validate_on_submit():
        appointment=Appointment.query.filter_by(id=form.id.data).first()

        # if appointment.date_time<=datetime.now():
        #     flash(f'Past Appointment cannot be canceled')
        #     return redirect(url_for('appt_cancel'))
        
        db.session.delete(appointment)
        db.session.commit()
        doctor=Doctor.query.filter_by(id=appointment.doctor_id).first()
        flash(f'Appointment {appointment.date_time} with {doctor} successfully cancelled')
        return redirect(url_for('index'))
    return render_template('appt_cancel.html',title='Cancel Appointment',form=form)