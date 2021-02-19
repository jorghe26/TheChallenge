import gpxpy
import pandas as pd
import random
from randomWalk import randomWalk


def test_data(gpx_filename,numData,numN):
    df = pd.DataFrame(columns=['time', 'lon', 'lat', 'fuel_con', 'ballast_water', 'fuel_rem'])
    deadData=[0]*(numData-numN)
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    gps_data = gpx.waypoints
    
    fc = randomWalk(170, len(gps_data)*numN)
    deadData=[fc[len(fc)-1]]*(numData-numN)
    fc.extend(deadData)
    i = 0

    for point in gps_data:
        df = df.append({'lon': point.longitude, 'lat': point.latitude, 'time': point.time,
                       'fuel_con': fc[i*numN:i*numN+numData], 'ballast_water': random.randint(100, 300),
                        'fuel_rem': random.randint(10, 200),'counter': i}, ignore_index=True)
        i+=1
    return df

#print(test_data("test.gpx")['fuel_con'][1])