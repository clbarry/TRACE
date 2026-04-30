"""
load_data.py
--------------------
Loads the session data and video file used throughout the dashboard.
To use your own data, update EXCEL_PATH and VIDEO below.

Place Excel files in `data/` and video files in `assets/data_video/`
(videos must live under `assets/` to be served to the browser).

EXPECTED DATA FORMAT
--------------------
One row per time sample, with at minimum these columns:
    - timestamp : datetime for that second
    - lf_coh    : low-frequency physiological concordance value (0–1)
    - hf_coh    : high-frequency physiological concordance value (0–1)
    - leading   : who is leading at that second ("C..." for child,
                  "P..." for parent)
    - cje       : 1 if Coordinated Joint Engagement is occurring, else null/0
    - sje       : 1 if Supported Joint Engagement is occurring, else null/0

If your column names differ, also update LEAD_COL, TS_COL, LF_COL, HF_COL
in app.py.
"""

import pandas as pd

# Path to the Excel data file
EXCEL_PATH = "data/"

# Which worksheet to load (0 = 1st sheet, 1 = 2nd sheet, etc.)
SHEET = 2

# Load the dataframe
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET)

# Path to the session video (must be under assets/ to be served)
VIDEO = "assets/data_video/"