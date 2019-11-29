
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from utilities import *

#daily_readings_data = read_data_from_file('daily-readings_5691533.json')
daily_readings_url = "{}{}".format(
    'https://waterpoint-engine-challenge-dev.mybluemix.net/sensors/daily-readings/',
    '5691533'
)
daily_readings_data = read_data_from_url(daily_readings_url)
daily_readings_per_site_df = pd.DataFrame(daily_readings_data)
daily_readings_per_site_df['localDate'] = pd.to_datetime(
	daily_readings_per_site_df['localDate'])
daily_readings_6025_df= daily_readings_per_site_df[
	daily_readings_per_site_df['sensorBarcode'] == 6025]
daily_readings_7162_df= daily_readings_per_site_df[
	daily_readings_per_site_df['sensorBarcode'] == 7162]
daily_yield_readings_traces = [
	go.Bar(
		x=daily_readings_6025_df['localDate'],
		y=daily_readings_6025_df['yieldDaily'],
		name = '6025',
	),
	go.Bar(
		x=daily_readings_7162_df['localDate'],
		y=daily_readings_7162_df['yieldDaily'],
		name = '7162',
    )
]

daily_hours_readings_traces = [
    go.Bar(
        x=daily_readings_6025_df['localDate'],
        y=daily_readings_6025_df['activeHours'],
        name = '6025',
    ),
	go.Bar(
		x=daily_readings_7162_df['localDate'],
		y=daily_readings_7162_df['activeHours'],
		name = '7162',
	)
]


layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='Dash: A web application framework for Python.'),

    dcc.Graph(
        id='daily_readings_yield',
        figure=dict(
            data = daily_yield_readings_traces,
            layout = dict(
                title = 'Daily Readings',
                xaxis = dict(title = 'Days'),
                yaxis = dict(title = 'Daily Yield'),
                barmode = 'group'
            )
        )
    ),
    dcc.Graph(
        id='daily_readings_hours',
        figure=dict(
            data = daily_hours_readings_traces,
            layout = dict(
                title = 'Daily Readings',
                xaxis = dict(title = 'Days'),
                yaxis = dict(title = 'Active Hours'),
                barmode = 'group'
            )
        )
    ),

    dcc.Link('Home', href='/')
])
