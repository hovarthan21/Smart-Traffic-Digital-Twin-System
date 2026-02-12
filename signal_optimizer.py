def optimize_signal(vehicle_count):
    if vehicle_count > 50:
        return "🚦 Extend Green Signal (60 sec)"
    elif vehicle_count > 20:
        return "🚦 Normal Green Signal (40 sec)"
    else:
        return "🚦 Short Green Signal (20 sec)"
