import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import sensors, daily_readings


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    dcc.Link('Sensor Data', href='/apps/sensors'),
    html.Br(),
    dcc.Link('Daily Readings per Site', href='/apps/daily_readings'),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/sensors':
        return sensors.layout
    elif pathname == '/apps/daily_readings':
        return daily_readings.layout
    elif pathname == '/':
        return layout_index
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=False, port=5000, threaded=True)
