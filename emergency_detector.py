def detect_emergency(vehicle_count):
    
    if vehicle_count > 80:
        return "⚠ Possible Emergency Congestion"
    return "No Emergency"

