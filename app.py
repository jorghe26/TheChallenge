import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import gpxpy
import numpy as np

array=open('Fuel.txt','r')
a=[]
a=array.read()
a=a.split("\n")
array.close()
df2=pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
gpx_file = open('Hurtigruten.gpx', 'r')
gpx = gpxpy.parse(gpx_file)
gps_data = gpx.tracks[0].segments[0].points
df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
i = 0
j = 0
for point in gps_data:
    i = i + 1
    if i == 100:
        df = df.append({'lon': point.longitude, 'lat' : point.latitude, 'alt' : point.elevation, 'time' : point.time}, ignore_index=True)
        df2 = df.append({'lon': point.longitude, 'lat' : point.latitude, 'alt' : np.float64(a[j]), 'time' : point.time}, ignore_index=True)
        
        j = j+1
        #print(j)
        i = 0
fig = px.line_geo(lat=df["lat"], lon=df["lon"])
app = dash.Dash(__name__)
server = app.server
app.title = "The Challenge"
app.layout = html.Div(
    children=[
        html.H1(children="The Challenge",
                className=".header-title"),
        html.P(
            children="Jorgens og Lars bidrag til The Challenge",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df["lon"],
                        "y": df["lat"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "GPS track fra strava"},
            },
        ),
        dcc.Graph(
            figure=fig,
        ),
    ]
)
print(df2['lat'])
if __name__ == "__main__":
   # app.run_server(debug=True)
   x=0