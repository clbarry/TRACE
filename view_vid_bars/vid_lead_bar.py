# Behavior Bar Heatmap
# Import necessary libraries
import plotly.express as px
import pandas as pd
import numpy as np

# Identify the columns to be used
TS_COL = "timestamp"                # identifies the timestamp column
LF_COL = "lf_coh"                   # identifies the low frequency coherence column
HF_COL = "hf_coh"                   # identifies the high frequeny coherence column

# Color Scheme for Leading Dyad
    # NOTE coding for 1:C = Child Leading, 2:P = Parent Leading is coorelated to LEAD_COLORS
LEAD_COLORS = [
    [0.0,  "rgb(255, 255, 255)"],   # for z = 0
    [0.5,  "rgb(136,218,111)"],     # for z = 1
    [1.0,  "rgb(35,119,180)"],      # for z = 2
]

# Dyad Lead Behavior Bar Heatmap
def make_lead_bar_heatmap(df, minimal=False):
    df = df.copy()

    # clean coh columns (make them numbers, fill null vals with 0)
    for col in [LF_COL, HF_COL]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)                           # cleans the coherence columns to make them number and fill null values with 0
    df = df.sort_values("timestamp").reset_index(drop=True)                                     # sorts the values by the timestamp and resets the index in that order
    
    
    df["leading_num"] = df["leading"].str.upper().map({"C": 1, "P": 2}).fillna(0).astype(int)   # map leading column to numeric values for plotting, C=1, P=2, .astype(int) to ensure integer type
    # define the data for the heatmap
    lead = ["Leading"]                          # y = identifies leading_num as the rows in the heat map (y order must match z order of z)
    times = df['timestamp']                     # x = identifies timestamp as the x axis measure
    values = df[["leading_num"]].T.to_numpy()   # z = idenitifies values for each row of the heatmap from the df .T.to_numpy() to transpose column to row

    fig = px.imshow(
        values,
        x=times,
        y=lead,
        color_continuous_scale=LEAD_COLORS,
        aspect="auto",                  # sets the aspect ratio to automatic
        origin="lower",                 # sets the origin to the lower left corner
        zmin=0,                         # sets the min and max values for the color scale
        zmax=2,                         # sets the min and max values for the color scale
    )

    # Update layout based on minimal flag
    if minimal:
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True,
            height=30,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            dragmode=False,
            coloraxis_showscale=False  # hide the color scale/colorbar) 
        )
        fig.update_xaxes(
            showticklabels=False,
            ticks="",
            showgrid=False,
            zeroline=False,
        )
        fig.update_yaxes(
            showticklabels=False,
            ticks="",
            showgrid=False,
            zeroline=False,
        )
    else:
        fig.update_layout(
            margin=dict(l=50, r=20, t=20, b=20),
            autosize=True,
            height=40,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard
            dragmode=False,                     # disables drag to zoom on heatmap
            coloraxis_showscale=False           # hide the color scale/colorbar) 
        )
        fig.update_xaxes(
            showticklabels=True,
            ticks="outside",
            showgrid=True,
            zeroline=False,
            tickangle=45,
        )
        fig.update_yaxes(
            showticklabels=True,
            ticks="outside",
            showgrid=False,
            zeroline=False,
        )
        fig.update_layout(font=dict(family="Lato, sans-serif"))
   
    return fig
