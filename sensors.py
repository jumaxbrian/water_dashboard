import json
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

#app = dash.Dash()
general_sensor_data = None

def get_sensor_data(sensor_dict):
    results = [x["sensors"] for x in sensor_dict]
    return results

def get_grouped_sensor_data(input_list):
    output_lists = []
    counter = -1
    for sensors in input_list:
        counter += 1
#        print(counter)
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
#                    print(sensor["details"], sensor.get("mwater_id"), type)
                    selected_data["uptime"] = sensor["details"][0].get("sensor_uptime", 0)
                else:
#                    print(sensor["details"], sensor.get("mwater_id"))
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

def read_data_from_file(filename):  
    results = None
    with open(filename) as f:
        results = json.load(f)
        results = results["data"]
    return results
#    print(general_sensor_data)

general_sensor_data = read_data_from_file('sensors.json')
sensors_df = pd.DataFrame(data=general_sensor_data)
sensor_data = get_sensor_data(general_sensor_data)
sensor_data_hash_map = create_sensor_hashmap(general_sensor_data)
sensor_grouped_data = get_grouped_sensor_data(sensor_data)
sensor_grouped_df = get_grouped_sensor_dataframes(sensor_grouped_data)
sensor_grouped_df = hydrate_grouped_sensor_df(sensor_grouped_df, sensors_df)


app = dash.Dash()
traces = []
for df in sensor_grouped_df:
    df['uptime'].fillna(0, inplace=True)
    temp_trace = go.Bar(
        x=df['mwater_id'],
        y=df['count'],
        showlegend=False,
#        name = df['county'],
#        marker=dict(color='#FFD700') # set the marker color to gold
        marker=dict(
            color=df['uptime'], 
            colorscale="Viridis", 
            showscale=True,
            colorbar=dict(title="Uptime")
        ), # set the marker color to gold
        text=df['county']
    )
    traces.append(temp_trace)
    
    
    
    
#Daily read data
#---------------
daily_readings_data = read_data_from_file('daily-readings_5691533.json')
daily_readings_per_site_df = pd.DataFrame(daily_readings_data)
daily_readings_per_site_df['localDate'] = pd.to_datetime(daily_readings_per_site_df['localDate'])
daily_readings_6025_df= daily_readings_per_site_df[
        daily_readings_per_site_df['sensorBarcode'] == 6025
        ]
daily_readings_7162_df= daily_readings_per_site_df[
        daily_readings_per_site_df['sensorBarcode'] == 7162
        ]
daily_yield_readings_traces = [
    go.Bar(
        x=daily_readings_6025_df['localDate'],
        y=daily_readings_6025_df['yieldDaily'],
        name = '6025',
#        marker=dict(color='#FFD700') # set the marker color to gold
#        marker=dict(color=df['uptime']) # set the marker color to gold
#        text=df['uptime']
    ),
      go.Bar(
        x=daily_readings_7162_df['localDate'],
        y=daily_readings_7162_df['yieldDaily'],
        name = '7162',
#        marker=dict(color='#FFD700') # set the marker color to gold
#        marker=dict(color=df['uptime']) # set the marker color to gold
#        text=df['uptime']
    )
]      

daily_hours_readings_traces = [
    go.Bar(
        x=daily_readings_6025_df['localDate'],
        y=daily_readings_6025_df['activeHours'],
        name = '6025',
#        marker=dict(color='#FFD700') # set the marker color to gold
#        marker=dict(color=df['uptime']) # set the marker color to gold
#        text=df['uptime']
    ),
    go.Bar(
        x=daily_readings_7162_df['localDate'],
        y=daily_readings_7162_df['activeHours'],
        name = '7162',
#        mode = 'lines',
#        marker=dict(type='line', color='#FFD700'), # set the marker color to gold
#        yaxis='y2'
#        marker=dict(color=df['uptime']) # set the marker color to gold
#        text=df['uptime']
    )
]      
    
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='Dash: A web application framework for Python.'),

    dcc.Graph(
        id='sensors',
        figure=dict(
            data = traces,
            layout = dict(
                title = 'Sensor Data',
                barmode = 'stack',
                xaxis = dict(title = 'Site Ids', type='category'),
                yaxis = dict(title = 'Sensor Count')
            )
        )
    ),
    
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
    )
])

if __name__ == '__main__':
    app.run_server()


        
        
