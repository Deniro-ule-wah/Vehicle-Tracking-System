from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vehicle(db.Model):
    vehicle_id = db.Column(db.String(50), primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Float, default=0.0)
    governor_status = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='active')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    alerts = db.relationship('Alert', backref='vehicle', lazy=True)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50), db.ForeignKey('vehicle.vehicle_id'))
    alert_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)
    severity = db.Column(db.String(20), default='medium')