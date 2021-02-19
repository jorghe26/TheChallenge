import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from create_df import test_data
from randomWalk import randomWalk

df = test_data("test.gpx")
fig = px.line_geo(lat=df["lat"], lon=df["lon"])
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
fig_map = px.line_mapbox(lon=df['lon'], lat=df['lat'], zoom=2)
fig_map.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=3, mapbox_center_lat = 61,
    margin={"r":0,"t":0,"l":0,"b":0})
#fig_bar = px.bar(x=['fuel consumption', 'fuel remaining'], y=[df['fuel_con'][0], df['ballast_water'][0]])
fig_bar = px.bar(x=['fuel consumption']*len(df), y=df['fuel_con'],animation_frame=list(range(0,len(df))),range_y=[0,20])
fig_bar.update_layout(height=425, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
fig_fuel = go.Figure()
fig_fuel.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10},yaxis_title="Fuel consumption (g/kWh)",
                       xaxis_title="timestamp")


y = df['fuel_con']
x = list(range(0,len(y)))
x_rev = x[::-1]
y_upper = [ye + 0.7 for ye in y]
y_lower = [ye - 0.7 for ye in y]
y_lower = y_lower[::-1]

fig_fuel.add_trace(go.Scatter(
    x=x+x_rev,
    y=y_upper+y_lower,
    fill='toself',
    fillcolor='rgba(0,100,80,0.2)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    name='Fair',
))

fig_fuel.add_trace(go.Scatter(
    x=x, y=y,
    line_color='rgb(0,100,80)',
    name='Fuel consumption',
    showlegend=False,
))
fig_fuel.update_traces(mode='lines')

fig_fuel.update_layout(hovermode="x")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "The Challenge"
app.layout = html.Div([
    html.Div(
        children=[
            html.H1(children="The Challenge",
                    className=".header-title"),
            html.P(
                children="Eivind, Jørgen, and Lars's contribution to DNV GL - The Challenge")]),

    html.Div([
        dcc.Graph(
            figure=fig_map,
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(figure=fig_bar),
        dcc.Graph(figure=fig_fuel),
    ], style={'display': 'inline-block', 'width': '49%'}),

])


if __name__ == "__main__":
    app.run_server(debug=True)