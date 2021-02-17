import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import gpxpy

gpx_file = open('Hurtigruten.gpx', 'r')
gpx = gpxpy.parse(gpx_file)
gps_data = gpx.tracks[0].segments[0].points
df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
for point in gps_data:
    df = df.append({'lon': point.longitude, 'lat' : point.latitude, 'alt' : point.elevation, 'time' : point.time}, ignore_index=True)

fig = px.line_geo(lat=df["lat"], lon=df["lon"], projection="orthographic")

data = pd.read_csv("avocado.csv")
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&ddisplay=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    children=[
        html.H1(children="The Challenge"),
        html.P(
            children="Jørgen og Eivinds bidrag til The Challenge",
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

if __name__ == "__main__":
    app.run_server(debug=True)