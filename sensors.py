import random
import time
# If you want real OBD later:
# import obd

class SensorSource:
    def __init__(self, mode="mock"):
        self.mode = mode
        self.start_ts = time.time()
        self.last_read_ts = time.time()
        
        # State variables for realistic simulation
        self.odo_km = 2540.0
        self.fuel_liters = 25.0  # ~83% of 30L tank
        self.current_speed = 0.0
        self.speed_target = random.uniform(20, 100)
        self.coolant_c = 87.0
        self.battery_v = 13.8
        self.vibration_rms = 0.5

    def hours_driven(self):
        # naive “engine on” timer for prototype
        return (time.time() - self.start_ts) / 3600.0

    def read(self):
        if self.mode == "mock":
            # Calculate time delta
            now = time.time()
            dt_sec = max(0.1, now - self.last_read_ts)
            self.last_read_ts = now
            
            # Smoothly change speed target every 30-60 seconds
            if random.random() < 0.02:  # ~2% chance per read
                self.speed_target = random.uniform(10, 90)
            
            # Speed acceleration/deceleration (realistic)
            accel = 5.0  # kph/sec
            speed_delta = max(-accel * dt_sec, min(accel * dt_sec, self.speed_target - self.current_speed))
            self.current_speed = max(0, self.current_speed + speed_delta)
            
            # Add small noise to speed
            speed_noise = random.gauss(0, 1)
            actual_speed = max(0, self.current_speed + speed_noise)
            
            # Odometer increases based on actual speed (km = speed_kph * hours)
            odo_increase = actual_speed * (dt_sec / 3600.0)
            self.odo_km += odo_increase
            
            # Fuel consumption: ~7-8 L/100km (realistic)
            fuel_consumption_per_km = 0.075  # liters per km
            self.fuel_liters -= actual_speed * (dt_sec / 3600.0) * fuel_consumption_per_km
            self.fuel_liters = max(0, self.fuel_liters)
            
            # Coolant temp rises with speed, falls otherwise
            target_coolant = 85 + (actual_speed / 100) * 10  # 85-95°C
            coolant_delta = (target_coolant - self.coolant_c) * 0.3
            self.coolant_c += coolant_delta + random.gauss(0, 0.5)
            self.coolant_c = max(80, min(100, self.coolant_c))
            
            # Battery voltage slightly varies but stays stable
            self.battery_v = 13.8 + random.gauss(0, 0.1)
            
            # Vibration increases with speed
            base_vibration = actual_speed / 150  # higher speed = more vibration
            self.vibration_rms = base_vibration + random.gauss(0, 0.1)
            self.vibration_rms = max(0, self.vibration_rms)
            
            # Oil pressure based on speed (engine RPM proxy)
            oil_pressure = 100 + (actual_speed / 100) * 200  # 100-300 kPa
            oil_pressure += random.gauss(0, 5)
            
            fuel_pct = (self.fuel_liters / 30.0) * 100  # tank is 30L
            
            return {
                "speed_kph": actual_speed,
                "fuel_pct": max(0, min(100, fuel_pct)),
                "coolant_c": self.coolant_c,
                "oil_pressure_kpa": max(50, oil_pressure),
                "battery_v": self.battery_v,
                "vibration_rms": self.vibration_rms,
                "odo_km": self.odo_km,
                "hours_driven": self.hours_driven(),
                "ambient_c": random.gauss(28, 2),
                "dtc_present": False
            }

        # Example skeleton for OBD (uncomment if you wire it up)
        # data = {}
        # data["speed_kph"] = self.connection.query(obd.commands.SPEED).value.to("kph").magnitude
        # data["coolant_c"] = self.connection.query(obd.commands.COOLANT_TEMP).value.magnitude
        # data["rpm"] = self.connection.query(obd.commands.RPM).value.magnitude
        # data["fuel_pct"] = self.connection.query(obd.commands.FUEL_LEVEL).value.magnitude
        # data["dtc_present"] = len(self.connection.query(obd.commands.GET_DTC).value or []) > 0
        # data["hours_driven"] = self.hours_driven()
        # data["odo_km"] = 0  # needs separate handling or CAN PID
        # data["battery_v"] = 13.8  # use a voltage sensor or PID if available
        # data["oil_pressure_kpa"] = 250 # need analog sensor for this
        # data["ambient_c"] = 30
        # data["vibration_rms"] = 0.6 # from IMU on I2C/SPI
        # return data
