import numpy as np
import pandas as pd
from dash import Dash, html, dcc

# Identify data columns in the dataframe
LF_COL = "lf_coh"
HF_COL = "hf_coh"
THRESH = 0.5
SJE_COL = "sje"
CJE_COL = "cje"

def event_durations(mask):

    # given a boolean true/false for each second,
    # return a list of durations (in seconds) for each consecutive run of True

    durations = []
    current_run = 0

    for value in mask:
        if value:
            # we are inside a moment of concordance or je
            current_run += 1
        else:
            # we just ended a moment of concordance or je
            if current_run > 0:
                durations.append(current_run)
                current_run = 0

    # if the dataset ends while still in a run, close it
    if current_run > 0:
        durations.append(current_run)

    return durations


def compute_summary_metrics(df):
    # compute counts and average durations for:
    # - low frequency concordance
    # - high frequency concordance
    # - joint engagement

    # true where lf/hf concordance is at or above the threshold
    lf_bool = df[LF_COL] >= THRESH
    hf_bool = df[HF_COL] >= THRESH

    # joint engagement: either sje == 1 OR cje == 1
    je_bool = (df[SJE_COL] == 1) | (df[CJE_COL] == 1)

    # each duration is number of cells in that run bc each cell is 1 second
    lf_durs = event_durations(lf_bool)
    hf_durs = event_durations(hf_bool)
    je_durs = event_durations(je_bool)

    n_lf = len(lf_durs)
    n_hf = len(hf_durs)
    n_joint = len(je_durs)

    # average duration in seconds (cells)
    avg_lf = sum(lf_durs) / n_lf if n_lf > 0 else 0.0
    avg_hf = sum(hf_durs) / n_hf if n_hf > 0 else 0.0
    avg_joint = sum(je_durs) / n_joint if n_joint > 0 else 0.0

    return {
        "n_lf": n_lf,
        "n_hf": n_hf,
        "avg_lf": avg_lf,
        "avg_hf": avg_hf,
        "n_joint": n_joint,
        "avg_joint": avg_joint,
    }


def make_summary_table(df):
    for col in [SJE_COL, CJE_COL]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    m = compute_summary_metrics(df)

    cell_left = {
        "padding": "4px 8px",
        "borderBottom": "1px solid #ccc",
        "borderRight": "1px solid #ccc",
        "fontSize": "14px",
        "whiteSpace": "nowrap",
        "fontFamily": "Lato, sans-serif",
    }
    
    cell_right = {
        "padding": "4px 8px",
        "borderBottom": "1px solid #ccc",
        "fontSize": "14px",
        "fontFamily": "Lato, sans-serif",
    }

    rows = [
        (
            "Total Moments of Concordance",
            f"{m['n_lf']} Low Frequency, {m['n_hf']} High Frequency",
        ),
        (
            "Average Duration of Concordance",
            f"{m['avg_lf']:.1f} s Low Frequency, {m['avg_hf']:.1f} s High Frequency",
        ),
        (
            "Total Moments of Joint Engagement",
            f"{m['n_joint']}",
        ),
        (
            "Average Duration of Joint Engagement",
            f"{m['avg_joint']:.2f} s",
        ),
    ]

    return html.Table(
        style={"width": "100%", "borderCollapse": "collapse", "marginTop": "6px"},
        children=html.Tbody([
            html.Tr([
                html.Td(label, style=cell_left),
                html.Td(value, style=cell_right),
            ])
            for label, value in rows
        ]),
    )
