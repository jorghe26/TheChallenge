
def fuelRemaining(current_time_index, max_time_index):
    max_fuel = 100
    unit = max_fuel / max_time_index
    current_fuel = unit * (max_time_index - current_time_index)
    print(current_fuel)
    return current_fuel

fuelRemaining(20,30)

def speed(current_lat, current_lon, last_lat, last_lon):
    lat_change = abs(current_lat - last_lat)
    lon_change = abs(current_lon - last_lon)
    return lon_change + lat_change
    


