from flask import Flask, jsonify, request
from flask_cors import CORS
from models.database import db, Vehicle, Alert
from services.tracking import update_vehicle_position
from services.alerts import check_all_alerts
from config import Config
from utils.validation import validate_vehicle_data
import datetime

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        vehicles = Vehicle.query.all()
        return jsonify([{
            "vehicle_id": v.vehicle_id,
            "latitude": v.latitude,
            "longitude": v.longitude,
            "governor_status": v.governor_status,
            "speed": v.speed,
            "last_updated": v.last_updated.isoformat(),
            "status": v.status
        } for v in vehicles])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_location', methods=['POST'])
def update_location():
    try:
        data = request.json
        if not validate_vehicle_data(data):
            return jsonify({"error": "Invalid data format"}), 400
        
        vehicle = update_vehicle_position(data)
        check_all_alerts(vehicle)
        return jsonify({"status": "success", "vehicle_id": vehicle.vehicle_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vehicle/<vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify({
        "vehicle_id": vehicle.vehicle_id,
        "latitude": vehicle.latitude,
        "longitude": vehicle.longitude,
        "speed": vehicle.speed,
        "status": vehicle.status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)