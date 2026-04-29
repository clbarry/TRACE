#### Import Packages ####
import plotly.graph_objects as go
import plotly as plt
import datetime as dt
import numpy as np
import pandas as pd
from load_data import df     # import the main dataframe


#Define the constants for the data cleaning and plotting

# Identify the columns to be used
TS_COL = "timestamp"                # identifies the timestamp column
CJE_COL = "cje"                     # identifies the coordinated joint engagement (CJE) column
SJE_COL = "sje"                     # identifies the shared joint engagement (SJE) column

# Define choices for engagement column creation
CHOICES = [
    1,   # sje = 1 then new value = 1
    2    # cje = 1 then new value = 2
]

# Color Scheme for Behavioral Engagement
    # 0: No Engagement, 1: SJE, 2: CJE
BEHAVIOR_COLORS = [
    [0.0,  "rgb(235,206,203)"],         # for z = 0; No Engagement
    [0.5,  "rgb(230, 140, 130)"],       # for z = 1; SJE
    [1.0,  "rgb(217,89,108)"],          # for z = 2; CJE
]

## VIDEO BEHAVIORAL ENGAGEMENT BAR 
# Heatmap with Datetime Axis


def make_behavior_heat(df, minimal=False):
    # loads and cleans df for behavior heatmap
    df = df.copy()

    # Define conditions for engagement calculation
    CONDITION = [
        (df["sje"] == 1) & (df["timestamp"].notna()),                  # condition 1: if sje = 1 and timestamp exists
        (df["cje"] == 1) & (df["timestamp"].notna())                   # condition 2: if cje = 1 and timestamp exists
    ]

    # Create engagement column based on conditions (0: No Engagement, 1: SJE, 2: CJE)
    # Made into one colunn because only one engagement type can occur at a time; otherwise would need separate columns and another row for the heatmap
    df["engagement"] = np.select(       
        CONDITION,                                              # sets the conditions to check
        CHOICES,                                                # defines output values for each condition
        default=np.where(df["timestamp"].notna(), 0, np.nan)    # sets 0 only if timestamp exists, otherwise leave blank
    )

    # clean coh columns (make them numbers, fill null vals with 0)
    df = df.sort_values("timestamp").reset_index(drop=True)     # sorts the values by the timestamp and resets the index in that order

    # define the data for the heatmap
    engagement = ["Engagement"]                 # y = identifies Engagment as the title for the row(s) in the heat map (y order must match z order of z)
    times = df['timestamp']                     # x = identifies timestamp as the x axis measure
    values = df[["engagement"]].T.to_numpy()    # z = idenitifies values for each row of the heatmap from the df .T.to_numpy() to transpose column to row


    # create the heatmap figure
    fig = go.Figure(data=go.Heatmap(
            z=values,
            x=times,
            y=engagement,
            zmin=0,                         # sets the min and max values for the color scale
            zmax=2,                         # sets the min and max values for the color scale
            colorscale=BEHAVIOR_COLORS,     # uses the defined color scale for behavioral engagement
            showscale=False))               # hides the color scale for this plot

    fig.update_layout(
            margin=dict(l=40, r=8, t=4, b=16),  # left, right, top, bottom margins - to fit in container on dashboard
            autosize=True,                      # automatically adjusts size to fit container (here and in app.py); width could be used, but autosize is better for container
            height=40,                          # height of the plot (can adjust to fit in container on dashboard)
            showlegend=False,                   # no legend for this plot
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard
            dragmode=False                      # disables drag to zoom on heatmap
        )                              # make it transparent so when it is in app.py dashboard it will not show going beyond the container

    # Upadate layout for viewing in different tabs (minimal for video playback, else for home tab)
    if minimal:
        # video playback
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=20),   # no margins 
            autosize=True,
            height=70,
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard
            dragmode=False                      # disables drag to zoom on heatmap
        )
        fig.update_xaxes(
            showgrid=False,
            showline=False,                      # no lines  
            showticklabels=True,                 # show time labels on x-axis as bottom in the stack of heatmaps
            tickfont=dict(size=8),
            zeroline=False,
        )
        fig.update_yaxes(
            showgrid=False,
            showline=False,                     # no lines  
            showticklabels=False,               # hide y engagement labels
            ticks="",                           # Don't display y engagement labels: maybe on hover?
            zeroline=False,
        )
    else:
        # home tab: same as before
        fig.update_layout(
            margin=dict(l=40, r=8, t=4, b=16),
            autosize=True,
            height=40,
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard
            dragmode=False                      # disables drag to zoom on heatmap
        )
        fig.update_xaxes(
            tickfont=dict(size=8),
            showgrid=False,
        )
        fig.update_yaxes(
            tickfont=dict(size=11),
            showgrid=False,
        )
        fig.update_layout(font=dict(family="Lato, sans-serif"))


    return fig
