## VIDEO SYNCHRONY BAR 
# Heatmap with Datetime Axis
    # Heatmap with Datetime Axis Resources 
        # https://plotly.com/python/heatmaps/
    # Color Resources: 
        # https://plotly.com/python/builtin-colorscales

import plotly.graph_objects as go
import plotly as plt
import datetime as dt
import numpy as np
import pandas as pd

# Identify the columns to be used
TS_COL = "timestamp"                # identifies the timestamp column
LF_COL = "lf_coh"                   # identifies the low frequency coherence column
HF_COL = "hf_coh"                   # identifies the high frequeny coherence column


## VIDEO SYNCHRONY BAR 
# Heatmap with Datetime Axis
def make_synch_heat(df, minimal=False):
    df = df.copy()

    # clean coh columns (make them numbers, fill null vals with 0)
    for col in [LF_COL, HF_COL]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)       # cleans the coherence columns to make them number and fill null values with 0 
    df = df.sort_values("timestamp").reset_index(drop=True)                 # sorts the values by the timestamp and resets the index in that order
    labels = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()      # makes a string label for x-axis
    synch = ["Low Frequency", 'High Frequency'] # y = identifies lf_coh and hf_coh as the rows in the heat map (y order must match z order of z)
    times = df['timestamp']                     # x = identifies timestamp as the x axis measure      
    values = df[[LF_COL, HF_COL]].T.to_numpy()  # z = idenitifies values for each row of the heatmap from the df .T.to_numpy() to transpose column to row
    
    fig = go.Figure(
        data=go.Heatmap(
            z=values,
            x=times,
            y=synch,
            zmin=0,                             # sets the min and max values for the color scale
            zmax=1,                             # sets the min and max values for the color scale
            colorscale="BuPu",
            showscale=False,                    # legend off
        )
    )

    if minimal:
        # video playback
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),    # no margins 
            autosize=True,                      # automatically adjusts size to fit container in app.py; width could be used, but autosize is better for container
            height=70,                          # height of the plot (can adjust to fit in container on dashboard)
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard
            dragmode=False                      # disables drag to zoom on heatmap
        )                                                                
        fig.update_xaxes(
            showgrid=False,
            showline=False,
            showticklabels=False,
            ticks="",                           # Don't display time labels: maybe on hover?
            #tickfont=dict(size=8),
            zeroline=False,
        )
        fig.update_yaxes(
            showgrid=False,
            showline=False,
            showticklabels=False,               # hide y-axis labels for stacking of heatmaps in app.py
            ticks="",                           # Don't display High/Low freq labels: maybe on hover?
            zeroline=False,
        )

    else:
        fig.update_layout(
            margin=dict(l=40, r=8, t=4, b=16),
            autosize=True,
            height=80,
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard 
            dragmode=False                      # disables drag to zoom on heatmap
        )
        fig.update_xaxes(
            showticklabels=False,
            showgrid=False,
        )
        fig.update_yaxes(
            tickfont=dict(size=10),
            showgrid=False,
        )
        fig.update_layout(font=dict(family="Lato, sans-serif"))

    return fig