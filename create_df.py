import gpxpy
import pandas as pd
import random
from randomWalk import randomWalk
import numpy as np
from fuel import fuelRemaining


def test_data(gpx_filename):
    df = pd.DataFrame(columns=['time', 'lon', 'lat', 'fuel_con', 'ballast_water', 'grey_water',
                               'waste', 'fresh_water', 'lubricant', 'fuel_rem'])

    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    gps_data = gpx.waypoints

    #fc = randomWalk(170, len(gps_data))
    #co2 = randomWalk(140,len)
    i = 0

    max_time = len(gps_data)

    for point in gps_data:
        fuel_rem = fuelRemaining(i, max_time)
        df = df.append({'lon': point.longitude, 'lat': point.latitude, 'time': point.time,
                       'fuel_con': randomWalk(170, 300), 'ballast_water': random.randint(100, 400),
                        'grey_water': random.randint(30,50),'waste': random.randint(1, 30),
                        'fresh_water': random.randint(60,110), 'lubricant': random.randint(10, 45),
                        'fuel_rem': fuel_rem, 'CO2': randomWalk(140, 60)}, ignore_index=True)
        i+=1
    return df

#print(test_data("test.gpx"))