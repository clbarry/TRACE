# TRACE: Visualizing Parent-Child Physiological Concordance

This repository contains the source code for **TRACE** (Temporal Representation of Annotated-behavior and Concordance across Events), a visual analytics dashboard for exploring physiological concordance (PC) and behavioral interactions in parent-child dyads.

TRACE integrates moment-level indicators, aggregate summaries, and video-based navigation into a single dashboard, making PC data more interpretable for clinicians, researchers, and non-specialists. The system was designed to assess dyadic parent-child interactions involving typically developing children and children with autism, but the design blueprint is reusable for visualizing PC in other applied contexts (e.g., couples' dynamics, mealtime interactions).

For full design rationale, task analysis, and expert evaluation, please see our manuscript.

## Demo Video

*A demo video walking through TRACE's features will be added here.*

## Features

- **Home Summary view** — aggregate charts (bar chart of leading participant, violin plot of PC magnitude distribution, donut chart of joint engagement, summary table) and stacked physiological/behavioral heatmaps for temporal exploration.
- **Video Play view** — synchronized video playback aligned with stacked heatmaps and point-in-time visuals, allowing users to correlate raw video footage with quantitative signals.
- **Point-in-Time (PIT) views** — toggleable radial bar chart glyph for moment-level PC magnitude and custom behavioral cards for categorical context at a selected timestamp.
- **Linked brushing and cross-filtering** — clicking the heatmap updates PIT panels and filters the summary panels to a 30-second window around the selected point; clicking a participant's bar filters the violin and donut charts by who led concordance.

## 1. Prerequisites

- **Python 3.10+**
- The ability to create and activate a virtual environment (`venv`, `conda`, or similar).

## 2. Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/clbarry/TRACE.git
   cd TRACE
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   
   # OR
   .\venv\Scripts\activate      
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## 3. Data

The physiological and behavioral data used in our manuscript are from the enTRAIN study and are **not included in this repository**.

To run TRACE with your own data, place your files in the following locations and update `load_data.py` accordingly:

- **Session data (Excel):** `data/<your_filename>.xlsx`
- **Session video:** `assets/data_video/<your_filename>.mp4`

  *Video files must live under `assets/` to be served by the Dash app.*

### Expected data format

The Excel sheet should contain one row per time sample, with at minimum the following columns:

| Column      | Description                                                              |
| ----------- | ------------------------------------------------------------------------ |
| `timestamp` | Datetime for the sample                                                  |
| `lf_coh`    | Low-frequency physiological concordance value (0–1)                      |
| `hf_coh`    | High-frequency physiological concordance value (0–1)                     |
| `leading`   | Who is leading at that moment (`"C..."` for child, `"P..."` for parent)  |
| `cje`       | `1` if Coordinated Joint Engagement is occurring, else null/0            |
| `sje`       | `1` if Supported Joint Engagement is occurring, else null/0              |

If your file paths, sheet number, or column names differ, update the constants in `load_data.py` and `app.py` accordingly. See `load_data.py` for inline documentation.

## 4. Running the app

From the project root, with your virtual environment activated:

```bash
python app.py
```

Dash will start a local server at `http://127.0.0.1:8050/`. Open that URL in your browser.

## 5. Repository structure

```
TRACE/
├── app.py                    # Main Dash app and callbacks
├── load_data.py              # Data loading and file paths
├── requirements.txt
├── data/                     # Place your session data here
├── assets/
│   └── data_video/           # Place your session video here
├── view_summary/             # Aggregate charts (bar, violin, donut, table)
├── view_point_in_time/       # PIT glyph and behavioral cards
├── view_vid_bars/            # Stacked heatmap components
├── vid_heatmaps.py           # Combined stacked heatmaps
└── legend.py                 # Combined dashboard legend
```

## 6. Contact

For questions about TRACE, the underlying methodology, or potential collaborations, please reach out to:

- **Carey L. Barry** — c.barry@northeastern.edu
- **Julia Weppler** — weppler.j@northeastern.edu

## Acknowledgments

We thank Jane Adams for feedback and Natasha Yamane for sharing insights into the dataset and physiological concordance. This work draws on data from the enTRAIN study.
