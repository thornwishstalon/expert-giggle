# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
token = open(".mapbox_token").read()

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import sqlite3 as sql
from dash.dependencies import Input, Output


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sql.connect(db_file)
    except sql.Error as e:
        print(e)

    return conn


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


px.set_mapbox_access_token(token)

# fig = px.scatter_mapbox(collisions, lat="latitude", lon="longitude", size_max=15)
# fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)

#
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
#
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

years = {0: 2010, 1: 2011, 2: 2012, 3: 2013, 4: 2014, 5: 2015, 6: 2016, 7: 2017, 8: 2018, 9: 2019, 10: 2020}
categories = {1: "wrong side of road", 2: "automobile right of way", 3: "improper turning", 4: "speeding",
              5: "traffic signals and signs", 6: "dui"}

app.layout = html.Div(children=[
    html.H1(children='Crashboard'),
    html.Div([
        html.Div([
            html.Label('Year Slider'),
            dcc.RangeSlider(
                id='year-slider',
                min=0,
                max=10,
                marks={i: '{}'.format(years[i]) for i in range(0, 10)},
                value=[5, 10],
            )]
            , style={"margin-bottom": "20px"}
        ),
        html.Div([
            html.Label('Hours Slider'),
            dcc.RangeSlider(
                id='hour-slider',
                min=0,
                max=23,
                marks={i: '{}h'.format(str(i)) for i in range(0, 23)},
                value=[0, 23],
            )]
            , style={"margin-bottom": "20px"}
        ),
        html.Div([
            html.Label('categories'),
            dcc.Dropdown(
                id='categories',
                options=[
                    {'label': 'wrong side of road', 'value': 1},
                    {'label': 'automobile right of way', 'value': 2},
                    {'label': 'improper turning', 'value': 3},
                    {'label': 'speeding', 'value': 4},
                    {'label': 'traffic signals and signs', 'value': 5},
                    {'label': 'dui', 'value': 6}
                ],
                value=[1, 2, 3, 4, 5, 6],
                multi=True,
            )]
            , style={"margin-bottom": "20px"}
        ),
        html.Div([
            html.Label('Fatal Crashes only'),
            dcc.Checklist(
                id='checkboxes',
                options=[
                    {'label': 'only fatal crashes', 'value': 1},
                ],
                value=[],
                style={"margin-bottom": "20px"}
            )]
            , style={"margin-bottom": "20px"}
        ),

    ], style={'columnCount': 1, "margin": "20px"}),

    html.Div([
        dcc.Graph(
            id='map'
        )
    ], style={"margin-left": "20px"})
])


@app.callback(
    Output('map', 'figure'),
    Input('year-slider', 'value')
)
def update_figure(value):
    conn = create_connection('switrs.sqlite')
    query = '''SELECT latitude, longitude, collision_date FROM collisions where latitude is not null and longitude is not null and bicycle_collision = 1'''

    collisions = pd.read_sql(
        query,
        conn, parse_dates=["collision_date"])
    fig = px.scatter_mapbox(collisions, lat="latitude", lon="longitude", size_max=15)
    fig.update_layout(transition_duration=500)
    return fig





if __name__ == '__main__':
    app.run_server(debug=True)
