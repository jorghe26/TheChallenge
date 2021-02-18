import gpxpy
import pandas as pd
import random


def test_data(gpx_filename):
    df = pd.DataFrame(columns=['time', 'lon', 'lat', 'fuel_con', 'ballast_water'])

    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    gps_data = gpx.waypoints
    for point in gps_data:
        df = df.append({'lon': point.longitude, 'lat': point.latitude, 'time': point.time,
                       'fuel_con': random.random(), 'ballast_water': random.random()}, ignore_index=True)

    return df

test_data("test.gpx")