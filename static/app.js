const socket = io();

let activityData = Array.from({length: 12}).map(() => Math.random() * 100 + 20);
let maxSpeedSeen = 0;
let totalTraveled = 0;

const els = {
  speed: document.getElementById('speed'),
  fuel_pct: document.getElementById('fuel_pct'),
  coolant_c: document.getElementById('coolant_c'),
  oil_pressure_kpa: document.getElementById('oil_pressure_kpa'),
  battery_v: document.getElementById('battery_v'),
  vibration_rms: document.getElementById('vibration_rms'),
  odo_km: document.getElementById('odo_km'),
  hours_driven: document.getElementById('hours_driven'),
  alerts: document.getElementById('alerts'),
  sensorsList: document.getElementById('sensorsList'),
  fuel: document.getElementById('fuel'),
  cost: document.getElementById('cost'),
  max_speed: document.getElementById('max_speed'),
  traveled: document.getElementById('traveled')
}

socket.on('sensor_update', (payload) => {
  const s = payload.sensors;
  if (!s) return;

  // Update metrics
  const fuelLiters = s.fuel_pct * 30 / 100; // assume 30L tank
  els.fuel.textContent = fuelLiters.toFixed(2) + ' Ltr';
  els.cost.textContent = '₹' + (fuelLiters * 150).toFixed(0); // assume ₹150/L
  els.odo_km.textContent = s.odo_km.toFixed(1) + ' Km';
  
  if (s.speed_kph > maxSpeedSeen) maxSpeedSeen = s.speed_kph;
  els.max_speed.textContent = maxSpeedSeen.toFixed(1) + ' kph';
  
  totalTraveled += s.speed_kph / 3600; // approximate km per second
  els.traveled.textContent = (50 + totalTraveled % 20).toFixed(1) + ' Km'; // demo

  // Activity chart shift
  activityData.shift();
  activityData.push(s.speed_kph);
  if (chart && chart.data) {
    chart.data.datasets[0].data = [...activityData];
    chart.update('none');
  }

  // Populate active sensors with live values
  els.sensorsList.innerHTML = '';
  const sensorDisplay = [
    {name: '🛢️ Fuel', key: 'fuel_pct', format: (v) => v.toFixed(1) + '%'},
    {name: '⏱️ Speed', key: 'speed_kph', format: (v) => v.toFixed(1) + ' kph'},
    {name: '📍 Odometer', key: 'odo_km', format: (v) => v.toFixed(1) + ' km'},
    {name: '🌡️ Coolant', key: 'coolant_c', format: (v) => v.toFixed(1) + '°C'},
    {name: '🔋 Battery', key: 'battery_v', format: (v) => v.toFixed(2) + ' V'},
    {name: '⚙️ Oil Pressure', key: 'oil_pressure_kpa', format: (v) => v.toFixed(0) + ' kPa'},
    {name: '📡 Vibration', key: 'vibration_rms', format: (v) => v.toFixed(2)}
  ];
  
  sensorDisplay.forEach(sensor => {
    const div = document.createElement('div');
    div.className = 'sensor-status';
    const value = s[sensor.key];
    div.innerHTML = `<span class="name">${sensor.name}</span><span class="value">${sensor.format(value)}</span>`;
    els.sensorsList.appendChild(div);
  });

  // Alerts
  els.alerts.innerHTML = '';
  if (payload.alerts.length === 0) {
    const li = document.createElement('li');
    li.className = 'info';
    li.textContent = '✓ All systems normal';
    els.alerts.appendChild(li);
  } else {
    payload.alerts.forEach(a => {
      const li = document.createElement('li');
      li.className = a.level || 'info';
      li.textContent = `[${a.level.toUpperCase()}] ${a.message}`;
      els.alerts.appendChild(li);
    });
  }
});

// Activity chart
const ctx = document.getElementById('activityChart').getContext('2d');
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: Array.from({length: 12}).map((_, i) => (i - 11) + ' min'),
    datasets: [{
      label: 'Speed (kph)',
      data: activityData,
      borderColor: '#8a6ef8',
      backgroundColor: 'rgba(138,110,248,0.15)',
      fill: true,
      tension: 0.4,
      borderWidth: 2,
      pointRadius: 0,
      pointHoverRadius: 4
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { display: false }
    },
    scales: {
      x: { display: true, ticks: { font: { size: 10 } } },
      y: { beginAtZero: true, max: 100, ticks: { font: { size: 10 } } }
    }
  }
});
