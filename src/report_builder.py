# src/report_builder.py

import pandas as pd
import base64
import os
from datetime import datetime


def _image_to_base64(image_path: str) -> str:
    """
    Converts a PNG file to base64 string so it can be
    embedded directly in HTML — no external file dependencies.
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _get_kpis(df: pd.DataFrame) -> dict:
    """Extract key insights to display as KPI cards."""
    return {
        "total_companies":   len(df),
        "total_sectors":     df["Broad Sector"].nunique(),
        "top_sector":        df.groupby("Broad Sector")["Name"].count().idxmax(),
        "top_company":       df.loc[df["Market Cap"].idxmax(), "Name"],
        "avg_market_cap":    f"${df['Market Cap'].mean() / 1e9:.1f}B",
        "max_market_cap":    f"${df['Market Cap'].max() / 1e9:.1f}B",
        "top_earning_sector":df.groupby("Broad Sector")["Earnings/Share"].mean().idxmax(),
    }


def build_report(df: pd.DataFrame, charts_dir: str = "output/charts",
                 output_path: str = "report/index.html"):
    """
    Builds a self-contained HTML dashboard.
    All charts are embedded as base64 — no external dependencies.
    """

    os.makedirs("report", exist_ok=True)

    # Load all charts as base64
    charts = {
        "companies_per_sector":    "01_companies_per_sector.png",
        "avg_market_cap":          "02_avg_market_cap_per_sector.png",
        "market_cap_distribution": "03_market_cap_distribution.png",
        "top_10_companies":        "04_top_10_companies.png",
        "price_vs_earnings":       "05_price_vs_earnings.png",
    }

    chart_b64 = {}
    for key, filename in charts.items():
        path = os.path.join(charts_dir, filename)
        chart_b64[key] = _image_to_base64(path)

    # Get KPIs
    kpis = _get_kpis(df)

    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S&P 500 Financial EDA Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #f0f2f5;
            color: #333;
        }}

        /* ── Header ── */
        .header {{
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2rem; margin-bottom: 8px; }}
        .header p  {{ color: #a0aec0; font-size: 0.95rem; }}

        /* ── KPI Cards ── */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            padding: 32px 40px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .kpi-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-top: 4px solid #4299e1;
        }}
        .kpi-card .value {{
            font-size: 1.6rem;
            font-weight: 700;
            color: #2b6cb0;
            margin-bottom: 6px;
        }}
        .kpi-card .label {{
            font-size: 0.8rem;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* ── Charts ── */
        .charts-section {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 40px 40px;
        }}
        .section-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #2d3748;
            margin: 32px 0 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .chart-card {{
            background: white;
            border-radius: 10px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .chart-card h3 {{
            font-size: 1rem;
            color: #4a5568;
            margin-bottom: 16px;
        }}
        .chart-card img {{
            width: 100%;
            height: auto;
            border-radius: 6px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }}

        /* ── Footer ── */
        .footer {{
            text-align: center;
            padding: 24px;
            color: #a0aec0;
            font-size: 0.85rem;
            border-top: 1px solid #e2e8f0;
        }}

        @media (max-width: 768px) {{
            .chart-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 1.4rem; }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <div class="header">
        <h1>S&P 500 Financial EDA Dashboard</h1>
        <p>Exploratory Data Analysis · {kpis['total_companies']} Companies · 
           {kpis['total_sectors']} Sectors · Generated {datetime.now().strftime('%B %d, %Y')}</p>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="value">{kpis['total_companies']}</div>
            <div class="label">Total Companies</div>
        </div>
        <div class="kpi-card">
            <div class="value">{kpis['total_sectors']}</div>
            <div class="label">GICS Sectors</div>
        </div>
        <div class="kpi-card">
            <div class="value">{kpis['top_sector']}</div>
            <div class="label">Largest Sector</div>
        </div>
        <div class="kpi-card">
            <div class="value">{kpis['top_company']}</div>
            <div class="label">Highest Market Cap</div>
        </div>
        <div class="kpi-card">
            <div class="value">{kpis['avg_market_cap']}</div>
            <div class="label">Avg Market Cap</div>
        </div>
        <div class="kpi-card">
            <div class="value">{kpis['max_market_cap']}</div>
            <div class="label">Max Market Cap</div>
        </div>
        <div class="kpi-card">
            <div class="value">{kpis['top_earning_sector']}</div>
            <div class="label">Top Earning Sector</div>
        </div>
    </div>

    <!-- Charts -->
    <div class="charts-section">

        <div class="section-title">Sector Analysis</div>
        <div class="chart-grid">
            <div class="chart-card">
                <h3>Number of Companies per Sector</h3>
                <img src="data:image/png;base64,{chart_b64['companies_per_sector']}" 
                     alt="Companies per Sector">
            </div>
            <div class="chart-card">
                <h3>Average Market Cap per Sector (USD Billions)</h3>
                <img src="data:image/png;base64,{chart_b64['avg_market_cap']}" 
                     alt="Avg Market Cap per Sector">
            </div>
        </div>

        <div class="section-title">Market Cap Distribution</div>
        <div class="chart-card">
            <h3>Market Cap Distribution per Sector — Box Plot</h3>
            <img src="data:image/png;base64,{chart_b64['market_cap_distribution']}" 
                 alt="Market Cap Distribution">
        </div>

        <div class="section-title">Company Highlights</div>
        <div class="chart-grid">
            <div class="chart-card">
                <h3>Top 10 Companies by Market Cap</h3>
                <img src="data:image/png;base64,{chart_b64['top_10_companies']}" 
                     alt="Top 10 Companies">
            </div>
            <div class="chart-card">
                <h3>Stock Price vs Earnings per Share by Sector</h3>
                <img src="data:image/png;base64,{chart_b64['price_vs_earnings']}" 
                     alt="Price vs Earnings">
            </div>
        </div>

    </div>

    <!-- Footer -->
    <div class="footer">
        Dataset: S&P 500 Companies Financials · 
        Built with Python, Pandas, Matplotlib, Seaborn · 
        Vikash Kumar — AI Architect Portfolio
    </div>

</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report saved to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")