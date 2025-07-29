import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import mplfinance as mpf

from datetime import datetime
import time
import jgtpy as jgt
from jgtpy import JGTCDS as cds
from jgtpy import JGTADS as ads
from jgtpy import adshelper as ah

from jgtpy import JGTPDSP as pds
from jgtpy.JGTChartConfig import JGTChartConfig
from jgtutils.jgtconstants import AO, AC, OPEN, HIGH, LOW, CLOSE, JAW, TEETH, LIPS


import os


main_plot_panel_id = 1
ao_plot_panel_id = 2
ac_plot_panel_id = 3

jaw_color = "#0000FF"
teeth_color = "#00FF00"
lips_color = "#FF0000"


def _make_alligator_line_plots_v2(data):
    jaw_plot = go.Scatter(
        x=data.index,
        y=data[JAW].values,
        # yaxis=f"y{main_plot_panel_id}",
        line=dict(color=jaw_color),
        mode="lines",
        name="Jaw",
    )
    teeth_plot = go.Scatter(
        x=data.index,
        y=data[TEETH].values,
        # yaxis=f"y{main_plot_panel_id}",
        line=dict(color=teeth_color),
        mode="lines",
        name="Teeth",
    )
    lips_plot = go.Scatter(
        x=data.index,
        y=data[LIPS].values,
        # yaxis=f"y{main_plot_panel_id}",
        line=dict(color=lips_color),
        mode="lines",
        name="Lips",
    )
    return jaw_plot, teeth_plot, lips_plot


def make_plot__ao_v5(data: pd.DataFrame, up_color="green", dn_color="red"):

    colors_ao = data["ao"].diff().apply(lambda x: up_color if x > 0 else dn_color)

    # Make 'ao' oscillator plot
    ao_plot = go.Bar(
        x=data.index,
        y=data["ao"].values,
        # yaxis=f"y{ao_plot_panel_id}",
        marker_color=colors_ao,
        name="AO",
    )

    return ao_plot


def make_plot__ac_v5(data: pd.DataFrame, up_color="darkgreen", dn_color="darkred"):

    colors_ac = data["ac"].diff().apply(lambda x: up_color if x > 0 else dn_color)

    # Make 'ac' oscillator plot
    ac_plot = go.Bar(
        x=data.index,
        y=data["ac"].values,
        # yaxis=f"y{ac_plot_panel_id}",
        marker_color=colors_ac,
        name="AC",
    )

    return ac_plot


def make_fig_v5():
    fig = make_subplots(
        rows=3,
        cols=3,
        column_widths=[0.13, 0.82, 0.05],
        row_heights=[0.6, 0.2, 0.2],
        row_titles=["Main", "AO", "AC"],
        shared_xaxes=True,
    )
    # fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4])
    return fig


def make_ohlc(data):
    ohlc_plot = go.Ohlc(
        x=data.index,
        open=data[OPEN],
        high=data[HIGH],
        low=data[LOW],
        close=data[CLOSE],
        # yaxis=f"y{main_plot_panel_id}",
    )
    return ohlc_plot


# timeframe = "D1"
# #i = "EUR/USD"
# instrument = "SPX500"

# no_cache=False

# data= ah.prepare_cds_for_ads_data(instrument=instrument,timeframe=timeframe)

# if no_cache or not os.path.exists("data.csv"):
#   data= ah.prepare_cds_for_ads_data(instrument=instrument,timeframe=timeframe)
#   data.to_csv("data.csv")
# else:
#   data=pd.read_csv("data.csv")


# Create Dash application
app = dash.Dash(__name__)  # Add the Flask application name

drop_down_instrument = dcc.Dropdown(
    id="instrument",
    options=[
        {"label": i, "value": i} for i in ["SPX500", "EUR/USD", "USD/JPY", "XAU/USD"]
    ],
    value="SPX500",
)
drop_down_timeframe = dcc.Dropdown(
    id="timeframe",
    options=[{"label": t, "value": t} for t in ["D1", "H4", "H1", "m15"]],
    value="D1",
)

# Define the app layout
chart_title = html.P(id="chart_title_p", children="JGT Interactive Learn Dash")
app.layout = html.Div(
    [
        dcc.Interval(
            id="interval-component",
            interval=1 * 60 * 1000,  # in milliseconds
            n_intervals=0,
        ),
        html.Table(
            [
                html.Tr(
                    id="",
                    className="",
                    children=[
                        html.Td(id="chart_title", className="", children=chart_title),
                        html.Td(id="", className="", children=drop_down_instrument),
                        html.Td(id="", className="", children=drop_down_timeframe),
                    ],
                ),
            ]
        ),
        dcc.Graph(id="live-graph", animate=True),
    ]
)


# Define callback to update graph
@app.callback(
    Output("live-graph", "figure"),
    [
        Input("interval-component", "n_intervals"),
        dash.dependencies.Input("instrument", "value"),
        dash.dependencies.Input("timeframe", "value"),
    ],
)
def update_graph_live(n, instrument, timeframe):
    # mpf_plot,axis,data = jgt.plot(instrument,timeframe,show=False)
    data = ah.prepare_cds_for_ads_data(instrument=instrument, timeframe=timeframe)

    # Make OHLC bars plot
    last_dt = str(data.index[-1])
    chart_title = " ADS Chart  " + instrument + " " + timeframe + " " + last_dt

    # jaw_plot,teeth_plot,lips_plot = make_plot_alligator(data)
    jaw_plot, teeth_plot, lips_plot = _make_alligator_line_plots_v2(data)

    ao_plot = make_plot__ao_v5(data, up_color="green", dn_color="red")

    ac_plot = make_plot__ac_v5(data, up_color="darkgreen", dn_color="darkred")

    ohlc_plot = make_ohlc(data)

    figure = make_fig_v5()

    figure.add_trace(jaw_plot, row=main_plot_panel_id, col=2)
    figure.add_trace(teeth_plot, row=main_plot_panel_id, col=2)
    figure.add_trace(lips_plot, row=main_plot_panel_id, col=2)

    # fig.add_trace(ao_plot, row=ao_plot_panel_id, col=1, secondary_y=False)
    # fig.add_trace(ao_plot, row=ao_plot_panel_id, col=1)
    figure.add_trace(ao_plot, row=ao_plot_panel_id, col=2)
    figure.add_trace(ac_plot, row=ac_plot_panel_id, col=2)

    figure.add_trace(ohlc_plot, row=main_plot_panel_id, col=2)

    figure.update_layout(
        autosize=True,
        xaxis_title="Date",
        yaxis_title="Price",
        # title=chart_title,
        height=1120,
        # Add your desired options here
        # For example:
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor="rgba(0,0,0,0)",
        # paper_bgcolor='rgba(0,0,0,0)',
        # font=dict(family='Courier New, monospace', size=18, color='#7f7f7f')
    )

    return figure


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8050, host="0.0.0.0")
