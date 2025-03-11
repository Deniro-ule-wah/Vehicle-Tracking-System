from models.database import db, Alert
from datetime import datetime, timedelta

class AlertConfig:
    INACTIVITY_THRESHOLD = timedelta(hours=72)
    SPEED_THRESHOLD = 80  # km/h

def check_all_alerts(vehicle):
    check_inactivity(vehicle)
    check_speed(vehicle)

def check_inactivity(vehicle):
    time_diff = datetime.utcnow() - vehicle.last_updated
    if time_diff > AlertConfig.INACTIVITY_THRESHOLD:
        create_alert(vehicle.vehicle_id, "inactivity", 
                    f"Vehicle inactive for {time_diff.days} days", "high")

def check_speed(vehicle):
    if vehicle.speed > AlertConfig.SPEED_THRESHOLD:
        create_alert(vehicle.vehicle_id, "overspeed",
                    f"Speed {vehicle.speed} exceeds threshold", "medium")

def create_alert(vehicle_id, alert_type, details, severity):
    alert = Alert(
        vehicle_id=vehicle_id,
        alert_type=alert_type,
        details=details,
        severity=severity
    )
    db.session.add(alert)
    db.session.commit()