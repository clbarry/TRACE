#Coherence Bars with imshowing video frames at those times
#Import necessary libraries
import pandas as pd
import numpy as np
import plotly.express as px


# Identify the columns to be used
TS_COL = "timestamp"                # identifies the timestamp column
LF_COL = "lf_coh"                   # identifies the low frequency coherence column
HF_COL = "hf_coh"                   # identifies the high frequeny coherence column

# Define function to create synchrony bar heatmap
def make_synch_bar_heatmap(df, minimal=False):
    df = df.copy()

    # clean coh columns (make them numbers, fill null vals with 0)
    for col in [LF_COL, HF_COL]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)       # cleans the coherence columns to make them number and fill null values with 0 
    df = df.sort_values("timestamp").reset_index(drop=True)                 # sorts the values by the timestamp and resets the index in that order
    labels = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()      # makes a string label for x-axis    df = main_df.copy()

    # clean coh columns (make them numbers, fill null vals with 0)
    for col in [LF_COL, HF_COL]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)       # cleans the coherence columns to make them number and fill null values with 0 
    df = df.sort_values("timestamp").reset_index(drop=True)                 # sorts the values by the timestamp and resets the index in that order
    labels = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()      # makes a string label for x-axis
    # Define frequency labels and extract timestamps
    synch = ["Low Frequency", 'High Frequency'] # y = identifies lf_coh and hf_coh as the rows in the heat map (y order must match z order of z)
    times = df['timestamp']                     # x = identifies timestamp as the x axis measure      

    # Extract coherence values for heatmap
    values = df[["lf_coh", "hf_coh"]].T.to_numpy()  # z = idenitifies values for each row of the heatmap from the df .T.to_numpy() to transpose column to row
    
    # Create heatmap figure
    fig = px.imshow(
        values,
        x=times,
        y=synch,
        color_continuous_scale="BuPu",
        aspect="auto",
        origin="lower",
        zmin=0,
        zmax=1,
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
            showgrid=False,
            showline=False,
            showticklabels=False,
            ticks="",
            zeroline=False,
        )
        fig.update_yaxes(
            showgrid=False,
            showline=False,
            showticklabels=False,
            ticks="",
            zeroline=False,
        )
    else:
        fig.update_layout(
            margin=dict(l=40, r=8, t=4, b=16),
            autosize=True,
            height=40,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            dragmode=False,
            coloraxis_showscale=False  # hide the color scale/colorbar) 
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
            showline=False,
        )
        fig.update_layout(font=dict(family="Lato, sans-serif"))


    return fig