def detect_emergency(vehicle_count):
    # Advanced version can detect ambulance class
    if vehicle_count > 80:
        return "⚠ Possible Emergency Congestion"
    return "No Emergency"
