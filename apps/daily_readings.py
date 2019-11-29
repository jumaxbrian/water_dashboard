
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from utilities import *

def convert_local_date_to_datetime(df):
    df['localDate'] = pd.to_datetime(df['localDate'])
    return df

def get_df_per_sensor_barcode(df):
    barcodes = df['sensorBarcode'].unique()
    results = []
    for val in barcodes:
        temp = df[df['sensorBarcode'] == val]
        results.append(dict(barcode=val, df=temp))
    return results

def get_daily_y_traces(sensor_data, y):
    results = []
    for data in sensor_data:
        temp = go.Bar(
            x=data['df']['localDate'],
            y=data['df'][y],
            name = str(data['barcode']),
        )
        results.append(temp)
    return results

def get_site_summary_data(url):
    results = []
    sensor_summary = read_data_from_url(url)
    sensor_summary = sensor_summary["sites"]
    for summary in sensor_summary:
        temp = dict(label=summary["site_name"], value=summary["mwater_id"])
        results.append(temp)
    default_val = temp["value"]
    return dict(default=default_val, site_summary=results)

def get_sensor_summary_url():
    return ("https://waterpoint-engine-challenge-dev.mybluemix.net/"
            "sensors/sites/summary")
    
def get_daily_readings_url(site_id):
    return ("https://waterpoint-engine-challenge-dev.mybluemix.net/"
            "sensors/daily-readings/{}").format(str(site_id))
    
def get_readings_for_plotting(site_id):
    """returns daily readings per barcode/sensor"""
    daily_readings_url = get_daily_readings_url(site_id)
    daily_readings_data = read_data_from_url(daily_readings_url)
    daily_readings_per_site_df = pd.DataFrame(daily_readings_data)
    daily_readings_per_site_df = convert_local_date_to_datetime(daily_readings_per_site_df)
    daily_readings_per_barcode_df = get_df_per_sensor_barcode(daily_readings_per_site_df)
    return daily_readings_per_barcode_df

sensor_summary_url = get_sensor_summary_url()
site_options = get_site_summary_data(sensor_summary_url)
layout = html.Div(children=[
        html.H1(children='Daily Reading Per Site'),
        html.Hr(),
        dcc.Link('Home', href='/'),
        html.Hr(),
        dcc.Dropdown(
            id='site-picker',
            options=site_options['site_summary'],
            value=site_options['default']
        ),
        dcc.Graph(id='daily_readings_yield'),
        dcc.Graph(id='daily_readings_hours'),
    ])

@app.callback(Output('daily_readings_yield', 'figure'),
    [Input('site-picker', 'value')])
def update_daily_readings_figure(selected_site):
    daily_readings_per_barcode_df = get_readings_for_plotting(selected_site)

    daily_yield_readings_traces = get_daily_y_traces(
        daily_readings_per_barcode_df, 'yieldDaily'
    )

    results = dict(
        data = daily_yield_readings_traces,
        layout = dict(
            title = 'Daily Readings',
            xaxis = dict(title = 'Days'),
            yaxis = dict(title = 'Daily Yield'),
            barmode = 'group'
        )
    )
    return results

@app.callback(Output('daily_readings_hours', 'figure'),
    [Input('site-picker', 'value')])
def update_daily_readings_figure(selected_site):
    daily_readings_per_barcode_df = get_readings_for_plotting(selected_site)

    daily_hours_readings_traces = get_daily_y_traces(
        daily_readings_per_barcode_df, 'activeHours'
    )

    results = dict(
        data = daily_hours_readings_traces,
        layout = dict(
            title = 'Daily Readings',
            xaxis = dict(title = 'Days'),
            yaxis = dict(title = 'Active Hours'),
            barmode = 'group'
        )
    )
    return results
