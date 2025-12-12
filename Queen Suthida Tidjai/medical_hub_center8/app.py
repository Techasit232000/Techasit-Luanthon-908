from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_hub_center8.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(30))
    phone = db.Column(db.String(50))
    notes = db.Column(db.Text)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
    datetime = db.Column(db.String(50))
    reason = db.Column(db.String(250))

@app.route('/')
def index():
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    next_appointments = Appointment.query.order_by(Appointment.id.desc()).limit(5).all()
    return render_template('index.html', total_patients=total_patients,
                           total_appointments=total_appointments, next_appointments=next_appointments)

# Patients
@app.route('/patients')
def patients():
    patients = Patient.query.order_by(Patient.id.desc()).all()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET','POST'])
def add_patient():
    if request.method == 'POST':
        p = Patient(
            first_name=request.form.get('first_name','').strip(),
            last_name=request.form.get('last_name','').strip(),
            dob=request.form.get('dob','').strip(),
            phone=request.form.get('phone','').strip(),
            notes=request.form.get('notes','').strip()
        )
        db.session.add(p)
        db.session.commit()
        flash('Patient added.', 'success')
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/patients/<int:patient_id>/edit', methods=['GET','POST'])
def edit_patient(patient_id):
    p = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        p.first_name = request.form.get('first_name', p.first_name)
        p.last_name = request.form.get('last_name', p.last_name)
        p.dob = request.form.get('dob', p.dob)
        p.phone = request.form.get('phone', p.phone)
        p.notes = request.form.get('notes', p.notes)
        db.session.commit()
        flash('Patient updated.', 'success')
        return redirect(url_for('patients'))
    return render_template('edit_patient.html', p=p)

# Appointments
@app.route('/appointments')
def appointments():
    appts = Appointment.query.order_by(Appointment.id.desc()).all()
    return render_template('appointments.html', appointments=appts)

@app.route('/appointments/add', methods=['GET','POST'])
def add_appointment():
    patients = Patient.query.order_by(Patient.first_name).all()
    if request.method == 'POST':
        appt = Appointment(
            patient_id=int(request.form.get('patient_id')),
            datetime=request.form.get('datetime','').strip(),
            reason=request.form.get('reason','').strip()
        )
        db.session.add(appt)
        db.session.commit()
        flash('Appointment added.', 'success')
        return redirect(url_for('appointments'))
    return render_template('add_appointment.html', patients=patients)

if __name__ == '__main__':
    # create database file if not exists
    if not os.path.exists('medical_hub_center8.db'):
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
