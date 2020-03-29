# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


header = html.H1(children="Social Distancing ABM")
description = html.Div(
    children="A model for simulating the effects of social distancing."
)
run_button = html.Button("Run", id="run-button")
output = html.P(id="output")
interval_div = html.Div(id="interval-div")
interval = dcc.Interval(id="interval", disabled=True)

app.layout = html.Div(children=[header, description, run_button, output, interval])


@app.callback(
    [Output("interval", "disabled")],
    [Input("run-button", "n_clicks"), Input("interval", "n_intervals")],
    [State("interval", "disabled")],
)
def toggle_interval(n_clicks, n_intervals, disabled):
    print(n_clicks, n_intervals, disabled)
    if n_clicks:
        if n_intervals:
            if n_intervals >= 10:
                return True
        else:
            return False
    else:
        return True


@app.callback(Output("output", "children"), [Input("interval", "n_intervals")])
def display_count(n):
    return f"Interval has fired {n} times"


if __name__ == "__main__":
    app.run_server(debug=True)
