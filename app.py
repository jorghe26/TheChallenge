import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from create_df import test_data
import json
import random


numDataF=300    #Number off data in plot, fuel
numNF=20        #Number of data between each position, fuel
numDataC=60     #CO2
numNC=5         #CO2
df = test_data("test.gpx",numDataF,numNF,numDataC,numNC)
df_2 = test_data("test2.gpx",numDataF,numNF,numDataC,numNC)

# fig = px.line_geo(lat=df["lat"], lon=df["lon"])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = ['track A', 'track B']
available_plots = ['fuel consumption', 'CO2 emissions']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "The Challenge"

app.layout = html.Div([
    html.Div(
        children=[
            html.H1(children="The Challenge",
                    className=".header-title"),
            html.P(
                children="Eivzzind, Jørgen, and Lars's contribution to DNV GL - The Challenge")]),
    html.Div(
        children=[
            html.Div([dcc.Dropdown(
                id='track',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='track A'
            ),
            ], style={'width': '20%', 'display': 'inline-block'}),
            html.Div([dcc.Dropdown(
                id='plot_s',
                options=[{'label': i, 'value': i} for i in available_plots],
                value='fuel consumption')], style={'width': '20%', 'display': 'inline-block', 'float': 'right'}), ],
        style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'},
    ),
    html.Div([
        dcc.Graph(
            id='map_plot',
            hoverData={'points': [{'customdata': [df['ballast_water'][0],
                                                  df['fuel_rem'][0],
                                                  df['grey_water'][0],
                                                  df['fresh_water'][0],
                                                  df['waste'][0],
                                                  df['lubricant'][0],
                                                  df['CO2'][0],
                                                  df['fuel_con'][0],
                                                  df['counter'][0]]
                                   }
                                  ]
                       }
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20 20 20'}),
    html.Div([
        dcc.Graph(id='graph_plot'),
        dcc.Graph(id='bar_plot'),
    ], style={'display': 'inline-block', 'width': '49%'}),



])

'''
@app.callback(
    dash.dependencies.Output('hover-data', 'children'),
    dash.dependencies.Input('map_plot', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)
'''

@app.callback(dash.dependencies.Output('map_plot', 'figure'),
              dash.dependencies.Input('track', 'value'))
def update_map_graph(track):
    if track == "track A":
        dff = df
    else:
        dff = df_2
    fig_map = px.line_mapbox(dff, lon=dff['lon'], lat=dff['lat'], custom_data=['ballast_water', 'fuel_rem',
                                                                               'grey_water', 'fresh_water', 'waste',
                                                                               'lubricant', 'CO2', 'fuel_con','counter'], zoom=2)
    fig_map.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=2, mapbox_center_lat=61,
                          margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_map


@app.callback(
    dash.dependencies.Output('bar_plot', 'figure'),
    dash.dependencies.Input('map_plot', 'hoverData'))
def update_bar_graph(hoverData):
    y_data = hoverData['points'][0]['customdata'][:-3]
    fig_bar = px.bar(x=['ballast_water', 'fuel_rem', 'grey_water', 'fresh_water', 'waste', 'lubricant'], y=y_data)
    fig_bar.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10}, showlegend=False, xaxis_title='',
                          yaxis_title='Amount loaded (liter)')
    fig_bar.update_yaxes(range=[0, 350])
    return fig_bar

dl=df
y_u=[]
y_l=[]
y_u2=[]
y_l2=[]
for i in range(len(dl)*numNF):
    y_u.append(random.randint(1,4))
    y_l.append(random.randint(1,4))
for i in range(len(dl)*numNF):
    y_u2.append(random.randint(1,4))
    y_l2.append(random.randint(1,4))
y_u.extend([1]*(numDataF-numNF))
y_l.extend([1]*(numDataF-numNF))
y_u2.extend([1]*(numDataC-numNC))
y_l2.extend([1]*(numDataC-numNC))


@app.callback(
    dash.dependencies.Output('graph_plot', 'figure'),
    [dash.dependencies.Input('map_plot', 'hoverData'),
     dash.dependencies.Input('plot_s', 'value')])
def update_graph(hoverData, plot_s):
    if plot_s == 'fuel consumption':

        yy = hoverData['points'][0]['customdata']
        y=yy[-2]
        x = list(range(0, len(y)))
        x_rev = x[::-1]
        y_upper = [ye + y_u[j] for ye,j in zip(y,range(yy[-1]*numNF,yy[-1]*numNF+numDataF))]
        y_lower = [ye - y_l[j] for ye,j in zip(y,range(yy[-1]*numNF,yy[-1]*numNF+numDataF))]
        y_lower = y_lower[::-1]

        fig_fuel = go.Figure()
        fig_fuel.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10},
                               yaxis_title="Fuel consumption (g/kWh)",
                               xaxis_title="Last 5 min (s)")

        fig_fuel.add_trace(go.Scatter(
            x=x + x_rev,
            y=y_upper + y_lower,
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='Confidence interval',
        ))
        fig_fuel.add_trace(go.Scatter(
            x=x, y=y,
            line_color='rgb(0,100,80)',
            name='Fuel consumption',
            showlegend=False,
        ))
        fig_fuel.update_traces(mode='lines')
    else:
        yy = hoverData['points'][0]['customdata']
        y=yy[-3]
        x = list(range(0, len(y)))
        x_rev = x[::-1]
        y_upper = [ye + y_u2[j] for ye,j in zip(y,range(yy[-1]*numNC,yy[-1]*numNC+numDataC))]
        y_lower = [ye - y_l2[j] for ye,j in zip(y,range(yy[-1]*numNC,yy[-1]*numNC+numDataC))]
        y_lower = y_lower[::-1]

        fig_fuel = go.Figure()
        fig_fuel.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10},
                               yaxis_title="CO2 emissions (g/tkm)",
                               xaxis_title="Last hour")

        fig_fuel.add_trace(go.Scatter(
            x=x + x_rev,
            y=y_upper + y_lower,
            fill='toself',
            fillcolor='rgba(199,58,2,0.2)',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='Confidence interval',
        ))
        fig_fuel.add_trace(go.Scatter(
            x=x, y=y,
            line_color='rgb(199,58,2)',
            name='CO2 emissions',
            showlegend=False,
        ))
        fig_fuel.update_traces(mode='lines')

    return fig_fuel

if __name__ == "__main__":
    app.run_server(debug=True)
