import pandas as pd

import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from utilities import *

general_sensor_data = None

def get_sensor_data(sensor_dict):
    results = [x["sensors"] for x in sensor_dict]
    return results

def get_grouped_sensor_data(input_list):
    output_lists = []
    counter = -1
    for sensors in input_list:
        counter += 1
        while len(sensors) > len(output_lists):
            output_lists.append([])

        for count, sensor in enumerate(sensors):
            selected_data = {
                    "install_date":sensor.get("install_date"),
                    "mwater_id": sensor.get("mwater_id"),
                    "removal_date": sensor.get("removal_date"),
                    "barcode": sensor.get("sensor_barcode"),
                    "count": 1,
            }
            if sensor["details"]:
                if type(sensor["details"]) is list:
                    selected_data["uptime"] = sensor["details"][0].get("sensor_uptime", 0)
                else:
                    selected_data["uptime"] = sensor["details"].get("sensor_uptime", 0)

            output_lists[count].append(selected_data)

    return output_lists

def hydrate_grouped_sensor_df(sensor_grouped_df, sensors_df):
    results = []
    for df in sensor_grouped_df:
        df = df.merge(sensors_df, on='mwater_id')
        df.drop(['sensors'], axis=1)
        results.append(df)

    return results

def create_sensor_hashmap(sensor_data):
    results = dict()
    for data in sensor_data:
        site_id = data['mwater_id']
        results[site_id] = data
        del results[site_id]['sensors']
    return results

def get_grouped_sensor_dataframes(sensor_grouped_data):
    results = []
    for data in sensor_grouped_data:
        df = pd.DataFrame(data)
        results.append(df)

    return results


#general_sensor_data = read_data_from_file('sensors.json')
sensor_data_url = "{}".format(
    "https://waterpoint-engine-challenge-dev.mybluemix.net/sensors"
)
general_sensor_data = read_data_from_url(sensor_data_url)
sensors_df = pd.DataFrame(data=general_sensor_data)
sensor_data = get_sensor_data(general_sensor_data)
sensor_data_hash_map = create_sensor_hashmap(general_sensor_data)
sensor_grouped_data = get_grouped_sensor_data(sensor_data)
sensor_grouped_df = get_grouped_sensor_dataframes(sensor_grouped_data)
sensor_grouped_df = hydrate_grouped_sensor_df(sensor_grouped_df, sensors_df)

traces = []
for df in sensor_grouped_df:
    df['uptime'].fillna(0, inplace=True)
    temp_trace = go.Bar(
        x=df['mwater_id'],
        y=df['count'],
        showlegend=False,
        marker=dict(
            color=df['uptime'],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Uptime")
        ),
        text=df['county']
    )
    traces.append(temp_trace)

layout = html.Div(children=[
    html.H1(children='Sensor Data'),
    html.Div(children='Dash: A web application framework for Python.'),

    dcc.Graph(
        id='sensors',
        figure=dict(
            data = traces,
            layout = dict(
                title = 'Sensors per Site',
                barmode = 'stack',
                xaxis = dict(title = 'Site Ids', type='category'),
                yaxis = dict(title = 'Sensor Count')
            )
        )
    ),

    dcc.Link('Home', href='/')
])
