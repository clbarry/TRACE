import plotly.graph_objects as go
import plotly as plt
import datetime as dt
import numpy as np
import pandas as pd

# Identify the columns to be used
TS_COL = "timestamp"                # identifies the timestamp column
LF_COL = "lf_coh"                   # identifies the low frequency coherence column
HF_COL = "hf_coh"                   # identifies the high frequeny coherence column

# Color Scheme for Leading Dyad
    # 1:C = Child Leading, 2:P = Parent Leading
    # White for 0 (no leading), Green for 1 (Child Leading), Blue for 2 (Parent Leading)
    # needed to make on a scale from 0 to 1 for colors, so set 0, 0.5, 1.0; in heatmap set zmin=0, zmax=2 to match leading_num values
LEAD_COLORS = [
    [0.0,  "rgb(255, 255, 255)"],   # for z = 0
    [0.5,  "rgb(136,218,111)"],     # for z = 1
    [1.0,  "rgb(35,119,180)"],      # for z = 2
]


## VIDEO DYAD LEAD BAR 
# Heatmap with Datetime Axis
def make_lead_heat(df, minimal=False):
    df = df.copy()

    # clean coh columns (make them numbers, fill null vals with 0)
    for col in [LF_COL, HF_COL]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)                           # cleans the coherence columns to make them number and fill null values with 0
    df = df.sort_values("timestamp").reset_index(drop=True)                                     # sorts the values by the timestamp and resets the index in that order
    #labels = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()                          # makes a string label for x-axis
    df["leading_num"] = df["leading"].str.upper().map({"C": 1, "P": 2}).fillna(0).astype(int)   # map leading column to numeric values for plotting
    # define the data for the heatmap
    lead = ["Leading"]                          # y = identifies leading_num as the rows in the heat map (y order must match z order of z)
    times = df['timestamp']                     # x = identifies timestamp as the x axis measure
    values = df[["leading_num"]].T.to_numpy()   # z = idenitifies values for each row of the heatmap from the df .T.to_numpy() to transpose column to row

    fig = go.Figure(data=go.Heatmap(
            z=values,
            x=times,
            y=lead,
            zmin=0,                         # sets the min and max values for the color scale
            zmax=2,                         # sets the min and max values for the color scale
            colorscale=LEAD_COLORS,         # uses the defined color scale for leading dyad
            showscale=False))               # hides the color scale for this plot


    if minimal:
        # video playback
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),    # no margins
            autosize=True,                      # automatically adjusts size to fit container (here and in app.py); width could be used, but autosize is better for container
            height=30,                          # height of the plot (can adjust to fit in container on dashboard)
            showlegend=False,                   # no legend for this plot
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard
            dragmode=False                      # disables drag to zoom on heatmap
        )                          # make it transparent so when it is in app.py dashboard it will not show going beyond the container

        fig.update_xaxes(
            showgrid=False,
            showline=False,
            showticklabels=False,               # hide x-axis labels for stacking of heatmaps in app.py
            ticks="",                           # Don't display time labels: maybe on hover?
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
            height=40,
            showlegend=False,                   # no legend for this plot
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard
            dragmode=False                      # disables drag to zoom on heatmap
        )

        fig.update_xaxes(
            tickfont=dict(size=8),
            showgrid=False,
            showticklabels=False,
            showline=False,
        )
        fig.update_yaxes(
            tickfont=dict(size=10),
            showgrid=False,
            showticklabels=True,
            showline=False,
        )
        fig.update_layout(font=dict(family="Lato, sans-serif"))

    return fig
