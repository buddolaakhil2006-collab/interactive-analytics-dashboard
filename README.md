# Interactive Analytics Dashboard — CodeNova Task 3

An interactive Streamlit dashboard for exploring fictional retail sales. Date, category, region, and minimum line-item sales controls update KPI cards and Plotly charts together. Empty filter results show a friendly message instead of failing.

> **Data note:** CodeNova's assignment PDF did not include a sales dataset. This repository includes the fictional, deterministic sales data used in the earlier Task 1 analysis. It contains no real customer records.

## Features and deliverables

- `app.py` — filterable Streamlit application with gross revenue, profit, margin, order-based AOV, units, monthly trend, category performance, sales-profit scatter, regional breakdown, and filtered data table.
- `data/sales_data.csv` — included sample data so the dashboard works after cloning.
- `assets/dashboard_walkthrough.gif` — visual walkthrough storyboard of changing example filter states; it is an illustrative preview, not a screen recording.
- `.streamlit/config.toml` — theme and hosting settings.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit opens the app at `http://localhost:8501`. No paid service, key, or external data source is needed. For free hosting, connect this repository to Streamlit Community Cloud and select `app.py`; this submission does not claim a live public deployment.

## Limitations

The data is synthetic, so findings are instructional rather than business evidence. AOV divides filtered revenue by distinct filtered orders. Filtering can remove some lines from an order, so it represents an average over the filtered rows rather than the complete original basket.
