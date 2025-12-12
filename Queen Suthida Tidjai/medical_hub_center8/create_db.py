from app import db, Patient, Appointment
db.create_all()
print("Database created with tables:", Patient.__tablename__, Appointment.__tablename__)
