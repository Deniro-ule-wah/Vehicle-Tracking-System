from backend.app import app, db
from backend.models.database import Vehicle
from datetime import datetime

with app.app_context():
    db.drop_all()
    db.create_all()

    # Sample data
    vehicles = [
        Vehicle(
            vehicle_id=f"VH00{i}",
            latitude=37.7749 + (i * 0.1),
            longitude=-122.4194 + (i * 0.1),
            speed=60.0 + (i * 5),
            governor_status=True,
            last_updated=datetime.utcnow(),
            status="active"
        ) for i in range(1, 4)
    ]
    
    db.session.add_all(vehicles)
    db.session.commit()
    print("Database initialized with sample data")