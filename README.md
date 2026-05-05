# Kasun Chamod — Cricket Stats Dashboard (Streamlit)

A Streamlit-hosted version of the modern single-page cricket dashboard
(`Cricket HTML/cricket-dashboard-modern/`). The look, layout, charts, filter
drawer and mobile bottom-tab bar are a 1:1 match with the original — only the
font has been changed: from the original Instrument Serif / Inter Tight /
JetBrains Mono trio to **Source Sans Pro** everywhere (loaded from Google
Fonts).

## What's inside

```
.
├── app.py                  # Streamlit entry point
├── dashboard_template.py   # Builds the full dashboard HTML
├── cricket_stats.xlsx      # ★ Match data — edit this in Excel
├── data.py                 # Loads the xlsx (with hardcoded fallback)
├── build_xlsx.py           # Re-generate the xlsx from data.py if needed
├── profile.jpg             # Player photo
├── requirements.txt
├── Dockerfile
└── README.md
```

`app.py` boots Streamlit, hides Streamlit's default chrome, and embeds the
entire dashboard via `streamlit.components.v1.html`. All client-side logic
(stat computation, chart rendering, filtering, sorting, tab switching) runs
inside the embedded page exactly as in the original.

The data flow is:

```
cricket_stats.xlsx  ──▶  data.py (loads via openpyxl)  ──▶  CRICKET_DATA
                                  │
              if missing/unreadable: falls back to a hardcoded
              copy of the same data baked into data.py
```

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` — the dashboard renders edge-to-edge.

## How it differs from the original HTML version

| Aspect             | Original (static HTML)                        | This (Streamlit)                                          |
|--------------------|-----------------------------------------------|-----------------------------------------------------------|
| Hosting            | Any static-file server                        | `streamlit run app.py`                                    |
| Vendor libs        | Bundled in `vendor/` (offline-capable)        | Loaded from public CDNs                                   |
| Data source        | `data.js` (JS literal)                        | `cricket_stats.xlsx`, with a `data.py` Python fallback   |
| Player photo       | `profile.jpg` next to HTML                    | Read once, base64-inlined into the page                   |
| Display font       | Instrument Serif + Inter Tight + JetBrains Mono | **Source Sans Pro** (loaded from Google Fonts)            |

Everything else — palette (cyan #22d3ee for batting, amber #f59e0b for
bowling, mint #34d399 for catches, ink #0a0e1a background), glass cards,
gradient mesh background, animated KPI counters, profile-ring pulse, chart
animations, sortable match log, filter chips, mobile bottom tab bar — is
preserved unchanged.

## Editing the data

The recommended workflow is the spreadsheet:

1. Open `cricket_stats.xlsx` in Excel (or LibreOffice, or Google Sheets after
   importing).
2. Add a new row at the bottom — fill in `Year`, `Opponent`, `Match_Type`,
   plus the batting and/or bowling columns. Leave the columns blank for any
   discipline the player didn't take part in.
3. Save the file. Refresh the dashboard in your browser — every stat
   re-derives.

Column reference:

| Column          | Notes                                                  |
|-----------------|--------------------------------------------------------|
| `Date`          | Optional — not used in stats                           |
| `Year`          | Required — drives the year filter                      |
| `Opponent`      | Free-form team name                                    |
| `Match_Type`    | Free-form format label (drives the format filter)      |
| `Runs`          | Leave blank if didn't bat                              |
| `Balls`         | Faced                                                  |
| `4s`, `6s`      | Boundaries                                             |
| `Out`           | `yes` or `no`                                          |
| `Dismissal`     | `LBW`, `Caught`, `Bowled`, `Run Out`, `Caught & Bowled`, `Stumped`, `Hit Wicket`, … |
| `Catch`         | Catches taken in the field this match                  |
| `Overs`         | Cricket-style: `7.4` = 7 overs 4 balls. Blank if didn't bowl |
| `Runs_Conceded` |                                                        |
| `Maidens`       |                                                        |
| `Wickets`       |                                                        |
| `matchId`       | Auto-filled if blank — leave it for new rows           |

If you'd rather keep everything in Python and skip the spreadsheet, edit the
`_FALLBACK_DATA` list at the bottom of `data.py` and either delete
`cricket_stats.xlsx` or run `python build_xlsx.py` to regenerate it from the
new Python data.

## Stats formulas (same as original)

| Stat              | Formula                                                                   |
|-------------------|---------------------------------------------------------------------------|
| Batting average   | total runs / total times out                                              |
| Strike rate       | (total runs / total balls) × 100                                          |
| Highest score     | max(Runs); appended `*` if not out                                        |
| 30+ / 50s / 100s  | innings where 30 ≤ Runs < 50, 50 ≤ Runs < 100, Runs ≥ 100                 |
| Bowling average   | total runs conceded / total wickets                                       |
| Bowling strike rate | total balls bowled / total wickets                                      |
| Economy           | total runs conceded / total overs                                         |
| Best bowling      | most wickets; ties broken by fewest runs                                  |
| 3W / 5W           | innings with Wickets ≥ 3 / Wickets ≥ 5                                    |
| Recent form       | last 5 matches in chronological order                                     |

Overs are stored cricket-style (`7.4` = 7 overs 4 balls) and converted to
balls for math.

## Deploying

Any host that runs Streamlit works:

- **Streamlit Community Cloud** — push to GitHub, point the dashboard at
  `app.py`. Free tier is fine for this size.
- **Render / Railway / Fly.io** — `streamlit run app.py --server.port $PORT`.
- **Docker** — `FROM python:3.11-slim`, copy the folder, `pip install -r
  requirements.txt`, `CMD ["streamlit", "run", "app.py", "--server.port=8501",
  "--server.address=0.0.0.0"]`.

Because the dashboard pulls Tailwind / Chart.js / Lucide / Microsport from
public CDNs, the deploy target needs outbound HTTPS — no extra build step
required.
