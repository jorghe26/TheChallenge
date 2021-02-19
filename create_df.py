import gpxpy
import pandas as pd
import random
from randomWalk import randomWalk


def test_data(gpx_filename):
    df = pd.DataFrame(columns=['time', 'lon', 'lat', 'fuel_con', 'ballast_water'])
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    gps_data = gpx.waypoints
    fc=randomWalk(10,len(gps_data))
    i=0
    for point in gps_data:
        df = df.append({'lon': point.longitude, 'lat': point.latitude, 'time': point.time,
                       'fuel_con': float(fc[i]), 'ballast_water': random.random()}, ignore_index=True)
        i+=1                   
    #print(df)
    return df
#test_data("test.gpx")