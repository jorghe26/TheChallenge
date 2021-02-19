import gpxpy
import pandas as pd
import random
from randomWalk import randomWalk
import numpy as np
from fuel import fuelRemaining
from fuel import speed


def test_data(gpx_filename):
    df = pd.DataFrame(columns=['time', 'lon', 'lat', 'fuel_con', 'ballast_water', 'fuel_rem', 'speed'])

    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    gps_data = gpx.waypoints

    fc = randomWalk(170, len(gps_data))
    i = 0

    max_time = len(gps_data)

    speed_array = np.zeros(max_time)
    counter = 1

    #TODO: init correctly
    last_lat = 0
    last_lon = 0
    current_lat = 0
    current_lon = 0

    for point in gps_data:
        vel = speed(current_lat, current_lon, last_lat, last_lon)
        last_lat = current_lat
        last_lon = current_lon
        fuel_rem = fuelRemaining(i,max_time)
        df = df.append({'lon': point.longitude, 'lat': point.latitude, 'time': point.time,
                       'fuel_con': randomWalk(170, 300), 'ballast_water': random.randint(100, 300),
                        'fuel_rem': fuel_rem, 'speed': vel}, ignore_index=True)
        i+=1
        current_lat = point.latitude
        current_lon = point.longitude
    return df

print(test_data("test.gpx"))