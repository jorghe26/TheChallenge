import gpxpy
import pandas as pd
import random
from randomWalk import randomWalk


def test_data(gpx_filename):
    df = pd.DataFrame(columns=['time', 'lon', 'lat', 'fuel_con', 'ballast_water', 'fuel_rem'])

    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    gps_data = gpx.waypoints

    fc = randomWalk(170, len(gps_data))
    i = 0

    for point in gps_data:
        df = df.append({'lon': point.longitude, 'lat': point.latitude, 'time': point.time,
                       'fuel_con': randomWalk(170, 300), 'ballast_water': random.randint(100, 300),
                        'fuel_rem': random.randint(10, 200)}, ignore_index=True)
        i+=1
    return df

print(test_data("test.gpx"))