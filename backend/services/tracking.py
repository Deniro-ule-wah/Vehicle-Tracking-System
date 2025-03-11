from models.database import db, Vehicle
from datetime import datetime

def update_vehicle_position(data):
    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        vehicle = Vehicle(vehicle_id=data['vehicle_id'])
    
    vehicle.latitude = data['latitude']
    vehicle.longitude = data['longitude']
    vehicle.speed = data.get('speed', 0.0)
    vehicle.governor_status = data.get('governor_status', True)
    vehicle.last_updated = datetime.utcnow()
    
    db.session.add(vehicle)
    db.session.commit()
    return vehicle