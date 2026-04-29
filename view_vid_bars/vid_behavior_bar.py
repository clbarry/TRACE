# Behavior Heatmap Bar with imshow for Video View
import plotly.express as px
import pandas as pd
import numpy as np

# Identify the columns to be used
TS_COL = "timestamp"                # identifies the timestamp column
CJE_COL = "cje"                     # identifies the coordinated joint engagement (CJE) column
SJE_COL = "sje"                     # identifies the shared joint engagement (SJE) column

# Define choices for engagement column creation
CHOICES = [
    1,   # sje = 1 then new value = 1
    2    # cje = 1 then new value = 2
]

BEHAVIOR_COLORS = [
    [0.0,  "rgb(235,206,203)"],         # for z = 0; No Engagement
    [0.5,  "rgb(230, 140, 130)"],       # for z = 1; SJE
    [1.0,  "rgb(217,89,108)"],          # for z = 2; CJE
]

# Define function to create behavior bar heatmap
def make_behavior_bar_heatmap(df, minimal=False):
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
    df = df.sort_values("timestamp").reset_index(drop=True)                                     # sorts the values by the timestamp and resets the index in that order
    labels = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()                          # makes a string label for x-axis

    # Define behavior labels and extract timestamps
    behaviors = ["Engagement"]                     # y = identifies engagement as the row in the heat map
    times = df['timestamp']                        # x = identifies timestamp as the x axis measure      

    # Extract engagement values for heatmap
    values = df[["engagement"]].T.to_numpy()      # z = idenitifies values for each row of the heatmap from the df .T.to_numpy() to transpose column to row
    
    # Create heatmap figure
    fig = px.imshow(
        values,
        x=times,
        y=behaviors,
        color_continuous_scale=BEHAVIOR_COLORS,
        aspect="auto",
        origin="lower",
        zmin=0,
        zmax=2,
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
            showticklabels=False,               # hide x-axis labels
            ticks="",                           # no ticks
            showgrid=False,                     # no gridlines
            zeroline=False,                     # no zero line
        )
        fig.update_yaxes(
            showticklabels=False,
            ticks="",
            showgrid=False,
            zeroline=False,
        )
    else:
        fig.update_layout(
            margin=dict(l=40, r=8, t=4, b=16),  # left, right, top, bottom margins - to fit in container on dashboard
            autosize=True,                      # automatically adjusts size to fit container (here and in app.py); width could be used, but autosize is better for container
            height=40,                          # height of the plot (can adjust to fit in container on dashboard)
            showlegend=False,                   # no legend for this plot
            paper_bgcolor="rgba(0,0,0,0)",      # transparent background to fit in dashboard
            plot_bgcolor="rgba(0,0,0,0)",       # transparent plot area to fit in dashboard
            dragmode=False,                     # disables drag to zoom on heatmap
            coloraxis_showscale=False           # hide the color scale/colorbar) 
        )                                       # make it transparent so when it is in app.py dashboard it will not show going beyond the container

        fig.update_xaxes(
            showgrid=False,
            showline=False,
            showticklabels=True,                 # show time labels on x-axis as bottom in the stack of heatmaps
            tickfont=dict(size=8),
            zeroline=False,
        )
        fig.update_yaxes(
            showgrid=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(size=8),
            zeroline=False,
        )
        fig.update_layout(font=dict(family="Lato, sans-serif"))

    return fig