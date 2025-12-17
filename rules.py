from dataclasses import dataclass

@dataclass
class Alert:
    level: str   # "info" | "warn" | "critical"
    code: str    # short key
    message: str # concise machine message

def evaluate(state: dict) -> list[Alert]:
    alerts = []
    s = state

    if s["coolant_c"] >= 100:
        alerts.append(Alert("critical","overheat","Engine temperature dangerously high. Stop safely."))
    elif s["coolant_c"] >= 95:
        alerts.append(Alert("warn","hot","Engine running hot. Reduce load and check coolant."))

    if s["fuel_pct"] <= 7:
        alerts.append(Alert("critical","fuel_empty","Fuel critically low. Refuel immediately."))
    elif s["fuel_pct"] <= 15:
        alerts.append(Alert("warn","fuel_low","Fuel low. Plan a refuel stop."))

    if s["battery_v"] < 12.0:
        alerts.append(Alert("warn","battery_low","Battery voltage low. Check alternator/battery."))

    if s["oil_pressure_kpa"] <= 150:
        alerts.append(Alert("critical","oil_pressure","Oil pressure low. Stop engine."))

    if s["hours_driven"] >= 12:
        alerts.append(Alert("info","fatigue","Long continuous drive detected (~12h). Take a rest."))

    if s.get("dtc_present"):
        alerts.append(Alert("warn","dtc","Diagnostic fault detected. Schedule service."))

    if s["vibration_rms"] > 1.2:
        alerts.append(Alert("warn","vibration","Excess vibration. Possible mount/bearing/road issue."))

    return alerts
