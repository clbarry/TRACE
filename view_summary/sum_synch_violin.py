# Violin plot of synchrony values

# https://plotly.com/python/violin/
# Color Scheme for the App
    # Colors from Plotly's 'BuPu' colorscale
    # Plotly colors: rgb(85, 4, 83) highest from Plotly's 'BuPu' colorscale


# Import Libraries
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import datetime as dt 
from plotly.subplots import make_subplots

# Identify the columns to be used
TS_COL = "timestamp"                # identifies the timestamp column
LF_COL = "lf_coh"                   # identifies the low frequency concordance column
HF_COL = "hf_coh"                   # identifies the high frequency concordance column

# Color Scheme 
BU_PU = px.colors.sequential.BuPu    # Plotly's 'BuPu' colorscale 

OUTLINE_COLOR = 'rgb(140, 107, 177)'      # lighter purple color from 'BuPu' colorscale for violin plot outline (LAST number is the transparency)
LINE_COLOR = 'rgb(85, 4, 83)'             # darkest color from 'BuPu' colorscale for violin plot outline and inner boxplot
VIOLIN_COLOR = 'rgb(191, 211, 230, 0.75)' # light blue from 'BuPu' colorscale for the fill of the violin plot


# Defines make_violin function 
def make_violin(df):  # pass df argument

    # clean coh columns (make them numbers, fill null vals with 0)
    for col in [LF_COL, HF_COL]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)       # cleans the concordance columns to make them number and fill null values with 0 
    df = df.sort_values("timestamp").reset_index(drop=True)                 # sorts the values by the timestamp and resets the index in that order
    

    # Calculate mean and median for hover info
    lf_mean = df["lf_coh"].mean()
    lf_median = df["lf_coh"].median()
    hf_mean = df["hf_coh"].mean()
    hf_median = df["hf_coh"].median()

    # Create subplots: 1 row, 2 columns
    fig = make_subplots(
        rows=1, cols=2,                                     # 1 row, 2 columns (1 row of 2 plots)  
        shared_yaxes=True,                                  # same concordance magnitude scale
        subplot_titles=("High Frequency Concordance", "Low Frequency Concordance"),     # titles for each subplot
        horizontal_spacing=0.05,
    )

    # LF concordance violin
    fig.add_trace(                                        # add trace to the figure means add a subplot to the figure
        go.Violin(
            y=df["lf_coh"],
            name='',
            fillcolor=VIOLIN_COLOR,                       # fill color of the violin plot
            line_color=OUTLINE_COLOR,                     # outline color of the violin plot
            marker=dict(color=LINE_COLOR, opacity=0.5),   # color of the inner boxplot markers
            box_visible=True,                             # show inner boxplot
            meanline_visible=True,                        # show mean line
            points="all",                                 # show all points (or "outliers" / False)
            jitter=0.2,                                   # spread points out
            hoveron="points",                             # show hover info on points only
            hovertemplate=(
            "Value: %{y:.3f}<br>"
            f"Mean: {lf_mean:.3f}<br>"
            f"Median: {lf_median:.3f}"
            "<extra></extra>"
           )
        ),
        row=1, col=2                                    # sets the position of this subplot in the figure (row 1, column 1
    )

    # HF concordance violin
    fig.add_trace(
        go.Violin(
            y=df["hf_coh"],
            name='',
            fillcolor=VIOLIN_COLOR,                       # fill color of the violin plot
            line_color=OUTLINE_COLOR,                     # outline color of the violin plot
            marker=dict(color=LINE_COLOR, opacity=0.5),   # color of the inner boxplot markers
            box_visible=True,                             # show inner boxplot
            meanline_visible=True,                        # show mean line
            points="all",                                 # show all points (or "outliers" / False)
            jitter=0.2,                                   # spread points out
            hoveron="points",                             # show hover info on points only
            hovertemplate=(                               # custom hover text (disable default hover text to reduce clutter)
            "Value: %{y:.3f}<br>"
            f"Mean: {hf_mean:.3f}<br>"
            f"Median: {hf_median:.3f}"
            "<extra></extra>"                              # custom hover text; %{y:.3f} - shows the y-value to 3 decimal places; <extra></extra> hides the gray box that usually shows the trace name
            ),
        
        ),
        row=1, col=1
    )
    

    # Customize x and y axes to have consistent look
    fig.update_xaxes(
        showgrid=False,               # no vertical gridlines
        gridcolor="lightgray",        # light gray gridlines
        title_text="",                # no x-axis title
        linecolor="lightgray",        # light gray x-axis line color
        linewidth=1,
        showticklabels=False,         # hide x-axis tick labels
        range=[-0.5, 0.5]             # fix x-axis range to violin width (added because the trace for the threashold for meaningful synchrony added a width to the x-axis)
        )

    fig.update_yaxes(
        showgrid=True, 
        gridcolor="lightgray", 
        title_text="",
        linecolor="lightgray",        # light gray y-axis line color
        title_standoff=15,
        linewidth=1)

    # Customize layout
    fig.update_yaxes(range=[0, 1], title_text="Concordance magnitude", row=1, col=1)

    fig.update_layout(
        title="Concordance Magnitude Distributions",
        font=dict(color="black"),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",       # main plotting background
        paper_bgcolor="rgba(0,0,0,0)",      # outer background
        autosize=True,                      # let Dash decide final size
        margin=dict(l=90, r=30, t=55, b=0), # reduce margins around plot to fit better
        hovermode="closest",                # only show hover info for closest point
        dragmode=False                      # disables drag to zoom on plot
    )

    # Add threshold lines as shapes (on top of violins)
    
    # Add threshold line for HF subplot
    fig.add_shape(
        type="line",
        xref="x", yref="y",         # xref="paper" spans subplot width (0 to 0.5 for left subplot)
        x0=-0.5, y0=0.5,            # line start point on x-axis (violin left edge; match plot span x-axis)
        x1=0.5, y1=0.5,             # line endpoint on x-axis (violin right edge; match plot span x-axis)
        line=dict(color=LINE_COLOR, width=2, dash="dash"),
        #row=1, col=1
    )

    # Add threshold line for LF subplot
    # Shape shows line across entire subplot width, but does not enable hover, so we add an invisible scatter trace below for hover info
    fig.add_shape(
        type="line",
        xref="x2", yref="y2",       # xref="x2",yref="y2" for second subplot
        x0=-0.5, y0=0.5,            # line start point on x-axis (violin 2 left edge; match plot span x-axis)
        x1=0.5, y1=0.5,             # line endpoint on x-axis (violin 2 right edge; match plot span x-axis)
        line=dict(color=LINE_COLOR, width=2, dash="dash"),
        #row=1, col=2           
    )


    # Annotation font for subplot titles
        # Updated to allow for different font sizes for the threashold annotation
    fig.update_annotations(
        font=dict(size=14, color="black"),
        selector=dict(text="High Frequency Concordance")  # Only update subplot titles
    )
    fig.update_annotations(
        font=dict(size=14, color="black"),
        selector=dict(text="Low Frequency Concordance")  # Only update subplot titles
    )
    fig.update_layout(font=dict(family="Lato, sans-serif"))

    return fig

