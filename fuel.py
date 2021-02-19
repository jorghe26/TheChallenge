
def fuelRemaining(current_time_index, max_time_index):
    max_fuel = 200
    unit = max_fuel / max_time_index
    current_fuel = unit * (max_time_index - current_time_index)
    return current_fuel

fuelRemaining(20,30)


