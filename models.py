from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timezone
import enum

db = SQLAlchemy()

class OrderStatus(enum.Enum):
    WAITING = "Waiting"
    ARRIVED = "Arrived"
    PICKED_UP = "Picked Up"

doctor_patient = db.Table(
    'doctor_patient',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'), primary_key=True)

)

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    name = db.Column(db.String, nullable =False)
    patient = db.relationship(
        'Patient',
        secondary = doctor_patient,
        back_populates = 'doctor'
    )

    #Sync with PatientOrder table
    orders = db.relationship('PatientOrder', back_populates = 'doctor')

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    date_of_birth = db.Column(db.Date, nullable = False)
    doctor = db.relationship(
        'Doctor',
        secondary = doctor_patient,
        back_populates = 'patient'
    )
    #Sync with PatientOrder table
    orders = db.relationship('PatientOrder', back_populates = "patient")
    

class PatientOrder(db.Model):
    __tablename__ = 'patient_order'
    id = db.Column(db.String, primary_key=True)
    brand = db.Column(db.String(100))
    bc = db.Column(db.Float)
    diameter = db.Column(db.Float)
    power = db.Column(db.Float)
    cylinder = db.Column(db.Float)
    axis = db.Column(db.Integer)
    add = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.WAITING)
    order_date = db.Column(db.Date, default=date.today())
    arrival_date = db.Column(db.Date, default=None)
    logs = db.relationship("Logs", backref='order', lazy=True)
    # Foreign keys to link to doctor and patient
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    # Relationships to access parent objects
    # "In 'Doctor' table update '.orders' attribute"
    # "In 'Patient' table update '.orders' attribute"
    doctor = db.relationship('Doctor', back_populates='orders')
    patient = db.relationship('Patient', back_populates='orders')


class stockOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    Power = db.Column(db.Float)
    cylinder = db.Column(db.Float)
    axis = db.Column(db.Integer)
    add = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=0)
    bc = db.Column(db.Float)
    diameter = db.Column(db.Float)
    order_date = db.Column(db.Date, default=date.today())
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.WAITING)
    arrival_date = db.Column(db.DateTime, default=None)


class Logs(db.Model):
    id = db.Column(db.String, primary_key=True)
    action = db.Column(db.String(100))       
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    order_id = db.Column(db.String, db.ForeignKey('patient_order.id'), nullable=False)
    # performed_by = db.Column(db.String(100))  # optional: track user who did it