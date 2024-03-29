# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import json
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import sqlite3 as sql
from dash.dependencies import Input, Output, State

token = open(".mapbox_token").read()


def get_continuous_color(colorscale, intermed):
    """
    Plotly continuous colorscales assign colors to the range [0, 1]. This function computes the intermediate
    color for any value in that range.

    Plotly doesn't make the colorscales directly accessible in a common format.
    Some are ready to use:

        colorscale = plotly.colors.PLOTLY_SCALES["Greens"]

    Others are just swatches that need to be constructed into a colorscale:

        viridis_colors, scale = plotly.colors.convert_colors_to_same_type(plotly.colors.sequential.Viridis)
        colorscale = plotly.colors.make_colorscale(viridis_colors, scale=scale)

    :param colorscale: A plotly continuous colorscale defined with RGB string colors.
    :param intermed: value in the range [0, 1]
    :return: color in rgb string format
    :rtype: str
    """
    if len(colorscale) < 1:
        raise ValueError("colorscale must have at least one color")

    if intermed <= 0 or len(colorscale) == 1:
        return colorscale[0][1]
    if intermed >= 1:
        return colorscale[-1][1]

    for cutoff, color in colorscale:
        if intermed > cutoff:
            low_cutoff, low_color = cutoff, color
        else:
            high_cutoff, high_color = cutoff, color
            break

    # noinspection PyUnboundLocalVariable
    return px.colors.find_intermediate_color(
        lowcolor=low_color, highcolor=high_color,
        intermed=((intermed - low_cutoff) / (high_cutoff - low_cutoff)),
        colortype="rgb")


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


def wrapData(options, overwrite=False):
    connection = create_connection('switrs.sqlite')
    for item in options:
        filename = 'input_dash/{}_collisions.csv'.format(item['label'])
        if not os.path.isfile(filename) or overwrite:
            # print(item['label'])
            query = '''SELECT * FROM collisions where 
                    collision_date IS NOT NULL and {} and bicycle_collision = 1'''  #
            collisions = pd.read_sql_query(query.format(item['value']), connection, parse_dates=["collision_date"])
            collisions.to_csv(filename, index=False)
    connection.close()


def calcSeverity(x):
    default = 10
    killed = x['bicyclist_injured_count'] * 2
    injured = x['bicyclist_killed_count']
    return default + injured * 3 + killed * 5


def has_deaths(row):
    if row['bicyclist_killed_count'] > 0:
        return 1
    return 0


def load_data(options):
    yearly_causes = []
    keys = []

    for item in options:
        print("loading {}".format(item['label']))
        collisions = pd.read_csv('input_dash/{}_collisions.csv'.format(item['label']), parse_dates=["collision_date"],
                                 dtype={
                                     'case_id': 'str',
                                     'killed_victims': 'Int64',
                                     'injured_victims': 'Int64',
                                     'bicyclist_injured_count': 'Int64',
                                     'bicyclist_killed_count': 'Int64',
                                     'bicycle_collision': 'Int64',
                                     'party_count': 'Int64',
                                     'pcf_violation_code': 'str',
                                     'pcf_violation_category': 'str',
                                     'latitude': 'float',
                                     'longitude': 'float',
                                     'state_route': 'str',  # ?
                                     'caltrans_district': 'str',  # ?
                                     'caltrans_district': 'str',  # ?
                                     'route_suffix': 'str',  # ?
                                 })

        # print(collisions.columns[24])
        collisions.dropna(subset=['collision_date', 'collision_time'], inplace=True)
        collisions['killed_victims'] = collisions['killed_victims'].fillna(0)
        collisions['killed_victims'] = collisions['killed_victims'].fillna(0)
        collisions['bicyclist_killed_count'] = collisions['bicyclist_killed_count'].fillna(0)
        collisions['bicyclist_injured_count'] = collisions['bicyclist_injured_count'].fillna(0)

        collisions['has_spatial_data'] = collisions['latitude']
        collisions['has_spatial_data'] = collisions['has_spatial_data'].apply(lambda x: 'n' if pd.isnull(x) else 'y')
        collisions['hour'] = pd.DatetimeIndex(collisions['collision_time']).hour
        collisions['month'] = pd.DatetimeIndex(collisions['collision_date']).month
        collisions['severity'] = 0
        collisions['severity'] = collisions.apply(lambda row: calcSeverity(row), axis=1)
        collisions['has_deaths'] = collisions.apply(lambda row: has_deaths(row), axis=1)
        # using dictionary to convert specific columns
        convert_dict = {'hour': int,
                        'month': int
                        }
        collisions = collisions.astype(convert_dict)
        collisions['year'] = int(item['label'])

        yearly_causes.append(collisions.reset_index().set_index('case_id'))
        keys.append(item['label'])

    return pd.concat(yearly_causes)


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

options = [
    {'label': '2010', 'value': 'collision_date between "2010-01-01" and "2010-12-31"'},
    {'label': '2011', 'value': 'collision_date between "2011-01-01" and "2011-12-31"'},
    {'label': '2012', 'value': 'collision_date between "2012-01-01" and "2012-12-31"'},
    {'label': '2013', 'value': 'collision_date between "2013-01-01" and "2013-12-31"'},
    {'label': '2014', 'value': 'collision_date between "2013-12-31" and "2015-01-01"'},
    {'label': '2015', 'value': 'collision_date between "2014-12-31" and "2016-01-01"'},
    {'label': '2016', 'value': 'collision_date between "2015-12-31" and "2017-01-01"'},
    {'label': '2017', 'value': 'collision_date between "2016-12-31" and "2018-01-01"'},
    {'label': '2018', 'value': 'collision_date between "2017-12-31" and "2019-01-01"'},
    {'label': '2019', 'value': 'collision_date between "2018-12-31" and "2020-01-01"'},
    {'label': '2020', 'value': 'collision_date between "2019-12-31" and "2021-01-01"'}
]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


px.set_mapbox_access_token(token)

years_labels = {0: 2010, 1: 2011, 2: 2012, 3: 2013, 4: 2014, 5: 2015, 6: 2016, 7: 2017, 8: 2018, 9: 2019, 10: 2020}
categories_labels = {1: "wrong side of road",
                     2: "automobile right of way",
                     3: "improper turning",
                     4: "speeding",
                     5: "traffic signals and signs",
                     6: "dui",
                     7: 'other hazardous violation',
                     8: 'unknown',
                     9: 'improper passing',
                     10: 'unsafe lane change',
                     11: 'unsafe starting or backing',
                     12: 'following too closely',
                     13: 'other than driver (or pedestrian)',
                     14: 'impeding traffic',
                     15: 'pedestrian violation',
                     16: 'other improper driving',
                     17: 'hazardous parking',
                     18: 'pedestrian right of way',
                     19: 'other equipment',
                     20: 'fell asleep',
                     21: 'brakes',
                     22: 'lights',
                     23: 'pedestrian dui',
                     }

category_color_map = {
    "wrong side of road": 'silver',
    "automobile right of way": 'maroon',
    "improper turning": 'teal',
    "speeding": 'orange',
    "traffic signals and signs": 'yellow',
    "dui": 'cadetblue',
    'other hazardous violation': 'cornflowerblue',
    'unknown': 'darksalmon',
    'improper passing': 'red',
    'unsafe lane change': 'aqua',
    'unsafe starting or backing': 'beige',
    'following too closely': 'burlywood',
    'other than driver (or pedestrian)': 'crimson',
    'impeding traffic': 'darkgoldenrod',
    'pedestrian violation': 'darkolivegreen',
    'other improper driving': 'darkorchid',
    'hazardous parking': 'deepskyblue',
    'pedestrian right of way': 'gold',
    'other equipment': 'springgreen',
    'fell asleep': 'plum',
    'brakes': 'lightgreen',
    'lights': 'lightblue',
    'pedestrian dui': 'hotpink'
}

twilight_colors, _ = px.colors.convert_colors_to_same_type(px.colors.cyclical.Twilight)
colorscale = px.colors.make_colorscale(twilight_colors)

app.layout = html.Div(children=[
    html.H1(children='road-rashboard 🚴 '),
    html.Div([
        html.Div([
            html.Label('Year Slider'),
            dcc.RangeSlider(
                id='year-slider',
                min=0,
                max=10,
                marks={i: '{}'.format(years_labels[i]) for i in range(0, 10)},
                value=[5, 10],
            )]
            , style={"marginBottom": "20px"}
        ),
        html.Div([
            html.Label('Hours Slider'),
            dcc.RangeSlider(
                id='hour-slider',
                min=0,
                max=23,
                marks={i: {'label': '{}h'.format(str(i)),
                           'style': {'color': get_continuous_color(colorscale, float(i) / 23)},
                           } for i in range(0, 23)},
                value=[0, 23],
            )]
            , style={"marginBottom": "20px"}
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
                    {'label': 'dui', 'value': 6},
                    {'label': 'other hazardous violation', 'value': 7},
                    {'label': 'unknown', 'value': 8},
                    {'label': 'improper passing', 'value': 9},
                    {'label': 'unsafe lane change', 'value': 10},
                    {'label': 'unsafe starting or backing', 'value': 11},
                    {'label': 'following too closely', 'value': 12},
                    {'label': 'other than driver (or pedestrian)', 'value': 13},
                    {'label': 'impeding traffic', 'value': 14},
                    {'label': 'pedestrian violation', 'value': 15},
                    {'label': 'other improper driving', 'value': 16},
                    {'label': 'hazardous parking', 'value': 17},
                    {'label': 'pedestrian right of way', 'value': 18},
                    {'label': 'other equipment', 'value': 19},
                    {'label': 'fell asleep', 'value': 20},
                    {'label': 'brakes', 'value': 21},
                    {'label': 'lights', 'value': 22},
                    {'label': 'pedestrian dui', 'value': 23}
                ],
                value=[1, 2, 3, 4, 5, 6],
                multi=True,
            )]
            , style={"marginBottom": "20px"}
        ),
        html.Div([
            html.Label('Severity Filter'),
            dcc.RadioItems(
                id='checkboxes',
                options=[
                    {'label': 'only fatal crashes', 'value': 1},
                    {'label': 'only injuries', 'value': 2},
                    {'label': 'all', 'value': 3},
                ],
                value=3,
                style={"marginBottom": "20px"}
            )]
            , style={"marginBottom": "20px"}
        ),

    ], style={'columnCount': 1}),
    html.Div(
        [
            dcc.Graph(
                id='map'
            )
            # dcc.Loading(
            #     id="loading_map",
            #     children=[
            #         dcc.Graph(
            #             id='map'
            #         )
            #     ],
            #     type="circle",
            #     fullscreen=False,
            # )
        ]
    ),

    html.Div([
        dcc.Loading(
            id="loading_state_total_chart",
            children=[
                dcc.Graph(
                    id='state_categories_pie'
                ),
            ],
            type="circle",
            fullscreen=False,
        ),
        dcc.Loading(
            id="loading_state_injury_chart",
            children=[
                dcc.Graph(
                    id='state_categories_pie_injuries'
                ),
            ],
            type="circle",
            fullscreen=False,
        ),
        dcc.Loading(
            id="loading_state_killed_chart",
            children=[

                dcc.Graph(
                    id='state_categories_pie_killed',
                ),
            ],
            type="circle",
            fullscreen=False,
        ),
        dcc.Loading(
            id="loading_total_chart",
            children=[
                dcc.Graph(
                    id='categories_pie'
                ),

            ],
            type="circle",
            fullscreen=False,
        ),
        dcc.Loading(
            id="loading_total_injury_chart",
            children=[
                dcc.Graph(
                    id='categories_pie_injuries'
                ),

            ],
            type="circle",
            fullscreen=False,
        ),
        dcc.Loading(
            id="loading_total_killed_chart",
            children=[
                dcc.Graph(
                    id='categories_pie_killed',
                )
            ],
            type="circle",
            fullscreen=False,
        ),

    ], style={'columnCount': 2}),
    dcc.Loading(
        id="loading_charts",
        children=[
            html.Div([
                dcc.Graph(
                    id='state_times_hist'
                ),
                dcc.Graph(
                    id='state_overall_timeline'
                ),
                dcc.Graph(
                    id='times_hist'
                ),
                dcc.Graph(
                    id='overall_timeline'
                )
            ], style={'columnCount': 2})
        ],
        type="circle",
        fullscreen=False,
    ),
    html.Div(
        [
            html.Footer(children=[
                # "Ⓒ Copyright 2021; made with dash, plotly and 🚀 by Fabian Pechstein",
                "made with dash, plotly and 🚀 by Fabian Pechstein",
                html.Br(),
                html.A(' write me', href="mailto:e0726104@student.tuwien.ac.at"),
                html.Br(),
                "Data by: ",
                html.A("California Traffic Collision Data from SWITRS ❤️ ",
                       href='https://www.kaggle.com/alexgude/california-traffic-collision-data-from-switrs',
                       target="_blank")

            ])
        ])

])


@app.callback(
    [
        #Output("map-chart", "selectedData"),
        Output('map', 'figure'),
        Output('categories_pie', 'figure'),
        Output('categories_pie_injuries', 'figure'),
        Output('categories_pie_killed', 'figure'),
        Output('times_hist', 'figure'),
        Output('overall_timeline', 'figure'),
        Output('state_categories_pie', 'figure'),
        Output('state_categories_pie_injuries', 'figure'),
        Output('state_categories_pie_killed', 'figure'),
        Output('state_times_hist', 'figure'),
        Output('state_overall_timeline', 'figure'),
    ],
    [
        Input('year-slider', 'value'),
        Input('hour-slider', 'value'),
        Input('checkboxes', 'value'),
        Input('categories', 'value'),
    ]
)
def update_figure(year_value, hour_value, checkboxes, categories):
    map_data = get_map_data(year_value, hour_value, checkboxes, categories)
    state_map_data = map_data.copy()
    # map data
    map_data.dropna(subset=['longitude', 'latitude'], inplace=True)
    fig = px.scatter_mapbox(map_data, lat="latitude", lon="longitude", color='hour', size='severity',
                            size_max=15, hover_name='collision_date',
                            color_continuous_scale=px.colors.cyclical.Twilight)

    fig.update_traces(customdata=map_data.index)
    fig.update_layout(transition_duration=700, clickmode='event+select', height=640)

    data = (map_data.groupby(
        ['pcf_violation_category'])
            .agg(count=('pcf_violation_category', 'count'),
                 bicycle_deaths=('bicyclist_killed_count', 'sum'),
                 bicycle_injured=('bicyclist_injured_count', 'sum')
                 )
            .reset_index()
            )
    data = data.sort_values(['count'], ascending=False)

    hist_data = (map_data.groupby(
        ['pcf_violation_category', 'hour'])
                 .agg(count=('pcf_violation_category', 'count'),
                      bicycle_deaths=('bicyclist_killed_count', 'sum'),
                      bicycle_injured=('bicyclist_injured_count', 'sum')
                      )
                 .reset_index()
                 )
    hist_data = hist_data.sort_values(['count'], ascending=False)

    state_data = (state_map_data.groupby(
        ['pcf_violation_category'])
                  .agg(count=('pcf_violation_category', 'count'),
                       bicycle_deaths=('bicyclist_killed_count', 'sum'),
                       bicycle_injured=('bicyclist_injured_count', 'sum')
                       )
                  .reset_index()
                  )
    state_data = state_data.sort_values(['count'], ascending=False)

    state_hist_data = (state_map_data.groupby(
        ['pcf_violation_category', 'hour'])
                       .agg(count=('pcf_violation_category', 'count'),
                            bicycle_deaths=('bicyclist_killed_count', 'sum'),
                            bicycle_injured=('bicyclist_injured_count', 'sum')
                            )
                       .reset_index()
                       )
    state_hist_data = state_hist_data.sort_values(['count'], ascending=False)

    return [fig, get_total_pie_chart(data, 'total spatial collisions: {}'),
            get_total_injured_pie_chart(data, 'total spatial injuries: {}'),
            get_total_kills_pie_chart(data, 'total spatial fatalities: {}'),
            get_time_hist(hist_data, 'spatial collisions by hour'),
            get_year_plot(map_data, 'weekly spatial bicycle collisions'),
            get_total_pie_chart(state_data, 'total statewide collisions: {}'),
            get_total_injured_pie_chart(state_data, 'total statewide injuries: {}'),
            get_total_kills_pie_chart(state_data, 'total statewide fatalities: {}'),
            get_time_hist(state_hist_data, 'statewide collisions by hour'),
            get_year_plot(state_map_data, 'weekly statewide bicycle collisions')
            ]


@app.callback(
    [
        Output('categories_pie', 'figure'),
        Output('categories_pie_injuries', 'figure'),
        Output('categories_pie_killed', 'figure'),
        Output('times_hist', 'figure'),
        Output('overall_timeline', 'figure'),
    ],
    [
        Input('map', 'selectedData'),
        State('year-slider', 'value'),
        State('hour-slider', 'value'),
        State('checkboxes', 'value'),
        State('categories', 'value'),
    ]
)
def display_selected_data(selected_data, year_value, hour_value, checkboxes, categories):
    print(selected_data)
    if selected_data is None:
        map_data = get_map_data(year_value, hour_value, checkboxes, categories)
        map_data.dropna(subset=['longitude', 'latitude'], inplace=True)
        data = (map_data.groupby(
            ['pcf_violation_category'])
                .agg(count=('pcf_violation_category', 'count'),
                     bicycle_deaths=('bicyclist_killed_count', 'sum'),
                     bicycle_injured=('bicyclist_injured_count', 'sum')
                     )
                .reset_index()
                )
        data = data.sort_values(['count'], ascending=False)

        hist_data = (map_data.groupby(
            ['pcf_violation_category', 'hour'])
                     .agg(count=('pcf_violation_category', 'count'),
                          bicycle_deaths=('bicyclist_killed_count', 'sum'),
                          bicycle_injured=('bicyclist_injured_count', 'sum')
                          )
                     .reset_index()
                     )
        hist_data = hist_data.sort_values(['count'], ascending=False)

        return [get_total_pie_chart(data, 'total spatial collisions: {}'),
                get_total_injured_pie_chart(data, 'total spatial injuries: {}'),
                get_total_kills_pie_chart(data, 'total spatial fatalities: {}'),
                get_time_hist(hist_data, 'spatial collisions by hour'),
                get_year_plot(map_data, 'weekly spatial collisions')]

    index = app_data.index
    ids = [p['customdata'] for p in selected_data['points']]

    selectedpoints = np.intersect1d(index, ids)

    data = app_data.loc[selectedpoints]

    pie_data = (data.groupby(
        ['pcf_violation_category'])
                .agg(count=('pcf_violation_category', 'count'),
                     bicycle_deaths=('bicyclist_killed_count', 'sum'),
                     bicycle_injured=('bicyclist_injured_count', 'sum')
                     )
                .reset_index()
                )
    pie_data = pie_data.sort_values(['pcf_violation_category'], ascending=False)

    hist_data = (data.groupby(
        ['pcf_violation_category', 'hour'])
                 .agg(count=('pcf_violation_category', 'count'),
                      bicycle_deaths=('bicyclist_killed_count', 'sum'),
                      bicycle_injured=('bicyclist_injured_count', 'sum')
                      )
                 .reset_index()
                 )
    hist_data = hist_data.sort_values(['count'], ascending=False)

    return [get_total_pie_chart(pie_data, 'total spatial collisions: {}'),
            get_total_injured_pie_chart(pie_data, 'total spatial injuries: {}'),
            get_total_kills_pie_chart(pie_data, 'total spatial fatalities: {}'),
            get_time_hist(hist_data, 'spatial collisions by hour'), get_year_plot(data, 'weekly spatial collisions')]


def get_total_pie_chart(data, title):
    total = data['count'].sum()
    pie = px.pie(data, values='count', names='pcf_violation_category', title=title.format(total),
                 color='pcf_violation_category',
                 color_discrete_map=category_color_map)
    pie.update_layout(transition_duration=500)

    return pie


def get_total_injured_pie_chart(data, title):
    total = data['bicycle_injured'].sum()
    pie = px.pie(data, values='bicycle_injured', names='pcf_violation_category',
                 title=title.format(total),
                 color='pcf_violation_category',
                 color_discrete_map=category_color_map)
    pie.update_layout(transition_duration=500)
    return pie


def get_total_kills_pie_chart(data, title):
    total = data['bicycle_deaths'].sum()
    pie = px.pie(data, values='bicycle_deaths', names='pcf_violation_category',
                 title=title.format(total),
                 color='pcf_violation_category',
                 color_discrete_map=category_color_map)
    pie.update_layout(transition_duration=500)
    return pie


def get_map_data(year_value, hour_value, checkboxes, categories):
    map_data = app_data

    if checkboxes == 1:
        map_data = map_data[(map_data['bicyclist_killed_count'] > 0)]
    if checkboxes == 2:
        map_data = map_data[(map_data['bicyclist_killed_count'] == 0)]

    cat = []
    for categoryId in categories:
        cat.append(categories_labels[categoryId])
    if 22 >= len(cat) > 0:
        map_data = map_data[(map_data['pcf_violation_category'].isin(cat))]

    map_data = map_data[
        (map_data['year'] >= int(years_labels[year_value[0]])) & (map_data['year'] <= int(years_labels[year_value[1]]))]
    map_data = map_data[
        (map_data['hour'] >= int(hour_value[0])) & (map_data['hour'] <= int(hour_value[1]))]
    return map_data


def get_time_hist(data, title):
    # return px.histogram(data, x="hour")
    fig = px.bar(data, x="hour", y="count", color='pcf_violation_category', barmode='stack',
                 color_discrete_map=category_color_map, title=title)

    return fig


def get_year_plot(map_data, title):
    year_data = map_data[['collision_date']]
    year_data.index = year_data['collision_date']

    return px.scatter(year_data.resample('W-MON').count()['collision_date'], y='collision_date',
                      title=title, labels={
            "index": "time",
            "collision_date": "count"
        }, )


if __name__ == '__main__':
    overwrite = False
    wrapData(options, overwrite=overwrite)
    app_data = load_data(options)

    app.run_server(debug=True)
