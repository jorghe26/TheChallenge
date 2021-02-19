
def fuelRemaining(current_time_index, max_time_index):
    max_fuel = 100
    unit = max_fuel / max_time_index
    current_fuel = unit * (max_time_index - current_time_index)
    print(current_fuel)
    return current_fuel

fuelRemaining(20,30)


