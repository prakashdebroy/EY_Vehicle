# Monkey patch BEFORE any other imports
try:
    import eventlet
    eventlet.monkey_patch()
except ImportError:
    pass

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from sensors import SensorSource
from rules import evaluate
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

source = None
shared_state = None
current = {"sensors": None, "alerts": []}


def set_shared_state(state_dict):
    """Allow main.py to set the shared state"""
    global shared_state
    shared_state = state_dict


def set_source(sensor_source):
    """Fallback for standalone mode"""
    global source
    source = sensor_source


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state')
def api_state():
    return jsonify(current)


def sensor_loop():
    global source, shared_state
    if not source:
        source = SensorSource(mode="mock")
    
    interval = 1.0
    while True:
        try:
            if shared_state:
                # Use shared state from main.py
                import threading
                with shared_state['lock']:
                    current['sensors'] = shared_state['sensors']
                    # Convert Alert objects to dictionaries for JSON serialization
                    current['alerts'] = [a.__dict__ for a in shared_state['alerts']]
            else:
                # Standalone mode: read directly
                sensors = source.read()
                alerts = evaluate(sensors)
                current['sensors'] = sensors
                current['alerts'] = [a.__dict__ for a in alerts]
            
            # Broadcast to all connected clients
            if current['sensors']:  # Only emit if we have data
                socketio.server.emit('sensor_update', 
                                    {'sensors': current['sensors'], 'alerts': current['alerts']}, 
                                    namespace='/')
            time.sleep(interval)
        except Exception as e:
            print(f"Sensor loop error: {e}")
            time.sleep(interval)


@socketio.on('connect')
def on_connect():
    # send current snapshot on connect
    if current['sensors']:
        socketio.emit('sensor_update', {'sensors': current['sensors'], 'alerts': current['alerts']})


if __name__ == '__main__':
    # start background sensor emitter
    socketio.start_background_task(sensor_loop)
    print("Starting dashboard on http://localhost:5001")
    socketio.run(app, host='0.0.0.0', port=5001, debug=False)
