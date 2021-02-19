import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from create_df import test_data
import json

df = test_data("test.gpx")
df_2 = test_data("test2.gpx")

#fig = px.line_geo(lat=df["lat"], lon=df["lon"])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = ['track A', 'track B']

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
    html.Div(
        html.Div([dcc.Dropdown(
                id='track',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='track A'
            ),
        ], style={'width': '49%', 'display': 'inline-block'}),
        style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'}
    ),
    html.Div([
        dcc.Graph(
            id='map_plot',
            hoverData={'points': [{'customdata': [df['ballast_water'][0],
                                                  df['fuel_rem'][0],
                                                  df['fuel_con']]}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='bar_plot'),
        dcc.Graph(id='graph_plot'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data')
        ])

])


@app.callback(
    dash.dependencies.Output('hover-data', 'children'),
    dash.dependencies.Input('map_plot', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(dash.dependencies.Output('map_plot', 'figure'),
              dash.dependencies.Input('track', 'value'))
def update_map_graph(track):
    if track == "track A":
        dff = df
    else:
        dff = df_2
    fig_map = px.line_mapbox(dff,lon=dff['lon'], lat=dff['lat'], custom_data=['ballast_water', 'fuel_rem', 'fuel_con'],zoom=2)
    fig_map.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=2, mapbox_center_lat=61,
                          margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_map

@app.callback(
    dash.dependencies.Output('bar_plot', 'figure'),
    dash.dependencies.Input('map_plot', 'hoverData'))
def update_bar_graph(hoverData):
    y_data = hoverData['points'][0]['customdata'][:2]
    fig_bar = px.bar(x=['ballast water','fuel remaining'], y=y_data)
    fig_bar.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10}, showlegend=False, xaxis_title='',
                          yaxis_title='Amount loaded (liter)')
    fig_bar.update_yaxes(range=[0, 350])
    return fig_bar


@app.callback(
    dash.dependencies.Output('graph_plot', 'figure'),
    dash.dependencies.Input('map_plot', 'hoverData'))
def update_graph(hoverData):
    y = hoverData['points'][0]['customdata'][-1]
    x = list(range(0, len(y)))
    x_rev = x[::-1]
    y_upper = [ye + 0.7 for ye in y]
    y_lower = [ye - 0.7 for ye in y]

    fig_fuel = go.Figure()
    fig_fuel.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10},
                           yaxis_title="Fuel consumption (g/kWh)",
                           xaxis_title="timestamp")

    fig_fuel.add_trace(go.Scatter(
        x=x + x_rev,
        y=y_upper + y_lower,
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

    return fig_fuel

if __name__ == "__main__":
    app.run_server(debug=True)
