def estimate_pollution(vehicle_count):
    co2 = vehicle_count * 2.3   
    if co2 > 150:
        level = "High Pollution"
    elif co2 > 60:
        level = "Moderate Pollution"
    else:
        level = "Low Pollution"
    return co2, level

