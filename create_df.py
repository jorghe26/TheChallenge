import gpxpy
import pandas as pd
import random
from randomWalk import randomWalk
import numpy as np
from fuel import fuelRemaining


def test_data(gpx_filename,numDataF,numNF,numDataC,numNC):
    df = pd.DataFrame(columns=['time', 'lon', 'lat', 'fuel_con', 'ballast_water', 'grey_water',
                               'waste', 'fresh_water', 'lubricant', 'fuel_rem'])

    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    gps_data = gpx.waypoints

    fc = randomWalk(170, len(gps_data)*numNF)
    fc2 = randomWalk(140, len(gps_data)*numNC)
    deadData=[fc[len(fc)-1]]*(numDataF-numNF)
    deadData2=[fc2[len(fc2)-1]]*(numDataC-numNC)
    fc.extend(deadData)
    fc2.extend(deadData2)
    #co2 = randomWalk(140,len)
    i = 0

    max_time = len(gps_data)

    for point in gps_data:
        fuel_rem = fuelRemaining(i, max_time)
        df = df.append({'lon': point.longitude, 'lat': point.latitude, 'time': point.time,
                       'fuel_con': fc[i*numNF:i*numNF+numDataF], 'ballast_water': random.randint(100, 400),
                        'grey_water': random.randint(30,50),'waste': random.randint(1, 30),
                        'fresh_water': random.randint(60,110), 'lubricant': random.randint(10, 45),
                        'fuel_rem': fuel_rem, 'CO2': fc[i*numNC:i*numNC+numDataC],'counter': i}, ignore_index=True)
        i+=1
    return df

#print(test_data("test.gpx"))