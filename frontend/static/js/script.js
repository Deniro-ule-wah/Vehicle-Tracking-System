const map = L.map('map').setView([37.7749, -122.4194], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

const markers = new Map();

function updateDashboard(data) {
    const vehicleList = document.getElementById('vehicle-list');
    vehicleList.innerHTML = '<h2>Vehicles</h2>' + data.map(v => `
        <div class="vehicle-item" data-id="${v.vehicle_id}">
            ${v.vehicle_id} - ${v.status} (${v.speed} km/h)
        </div>
    `).join('');

    // Update map markers
    data.forEach(vehicle => {
        const latlng = [vehicle.latitude, vehicle.longitude];
        if (markers.has(vehicle.vehicle_id)) {
            markers.get(vehicle.vehicle_id).setLatLng(latlng);
        } else {
            const marker = L.marker(latlng).addTo(map);
            marker.bindPopup(`
                <b>${vehicle.vehicle_id}</b><br>
                Speed: ${vehicle.speed} km/h<br>
                Status: ${vehicle.status}
            `);
            markers.set(vehicle.vehicle_id, marker);
        }
    });
}

function updateAlerts(alerts) {
    const alertList = document.getElementById('alert-list');
    alertList.innerHTML = alerts.slice(0, 5).map(alert => `
        <li class="alert-${alert.severity}">
            ${alert.alert_type}: ${alert.details} 
            (${new Date(alert.timestamp).toLocaleString()})
        </li>
    `).join('');
}

async function fetchData() {
    try {
        const [vehiclesRes, alertsRes] = await Promise.all([
            fetch('http://localhost:5000/vehicles'),
            fetch('http://localhost:5000/alerts')
        ]);
        
        const vehicles = await vehiclesRes.json();
        const alerts = await alertsRes.json();
        
        updateDashboard(vehicles);
        updateAlerts(alerts);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

setInterval(fetchData, 5000);
fetchData(); // Initial fetch