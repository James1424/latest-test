from __future__ import annotations

import pandas as pd

from config import (
    BACKTEST_START,
    BENCHMARK_COMPARISON_FILE,
    BENCHMARK_YEARLY_FILE,
    COMPONENT_CHANGES_FILE,
    CURRENT_TICKERS_FILE,
    DETAIL_FILE,
    MOMENTUM_WINDOWS,
    README_FILE,
    SUMMARY_FILE,
    WIKI_URL,
    YEARLY_RETURNS_FILE,
)


def fmt_pct(x) -> str:
    if pd.isna(x):
        return ""
    return f"{float(x) * 100:.2f}%"


def df_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No data available._"
    return df.to_markdown(index=False)


def format_yearly_table(yearly: pd.DataFrame, window: int) -> str:
    sub = yearly[yearly["momentum_window"] == window].copy()
    if sub.empty:
        return "_No yearly data available._"

    sub = sub.drop(columns=[c for c in sub.columns if c.endswith("Trades")], errors="ignore")
    sub = sub.drop(columns=["momentum_window"], errors="ignore")
    sub = sub.rename(columns={"year": "Year"})

    for col in sub.columns:
        if col != "Year":
            sub[col] = sub[col].map(fmt_pct)

    current_year = sub["Year"].max()
    sub["Year"] = sub["Year"].apply(lambda y: f"{int(y)} (YTD)" if y == current_year else int(y))

    return df_to_markdown(sub)


def format_summary(summary: pd.DataFrame, window: int) -> str:
    sub = summary[summary["momentum_window"] == window].copy()
    if sub.empty:
        return "_No summary data available._"

    # Removed "trades" from README display.
    sub = sub.drop(columns=["momentum_window", "trades"], errors="ignore")

    sub = sub.rename(
        columns={
            "top_n": "Top N",
            "holding_months": "Holding Months",
            "avg_return": "Avg Return",
            "median_return": "Median Return",
            "win_rate": "Win Rate",
            "best_return": "Best Return",
            "worst_return": "Worst Return",
            "avg_available_universe_size": "Avg Available Universe",
        }
    )

    for col in ["Avg Return", "Median Return", "Win Rate", "Best Return", "Worst Return"]:
        if col in sub.columns:
            sub[col] = sub[col].map(fmt_pct)

    if "Avg Available Universe" in sub.columns:
        sub["Avg Available Universe"] = sub["Avg Available Universe"].map(
            lambda x: f"{float(x):.1f}" if pd.notna(x) else ""
        )

    return df_to_markdown(sub)


def format_benchmark_comparison(comp: pd.DataFrame, window: int) -> str:
    sub = comp[comp["momentum_window"] == window].copy()
    if sub.empty:
        return "_No benchmark comparison available._"

    # Removed "years" from README display.
    sub = sub.drop(columns=["momentum_window", "years"], errors="ignore")

    sub = sub.rename(
        columns={
            "top_n": "Top N",
            "holding_months": "Holding Months",
            "avg_strategy_yearly_return": "Avg Strategy Yearly Return",
            "avg_qqq_yearly_return": "Avg QQQ Yearly Return",
            "avg_excess_return": "Avg Excess Return",
            "beat_rate_vs_qqq": "Beat Rate vs QQQ",
            "best_excess": "Best Excess",
            "worst_excess": "Worst Excess",
        }
    )

    for col in [
        "Avg Strategy Yearly Return",
        "Avg QQQ Yearly Return",
        "Avg Excess Return",
        "Beat Rate vs QQQ",
        "Best Excess",
        "Worst Excess",
    ]:
        if col in sub.columns:
            sub[col] = sub[col].map(fmt_pct)

    return df_to_markdown(sub)


def format_latest_selection(detail: pd.DataFrame, window: int) -> str:
    sub = detail[
        (detail["momentum_window"] == window)
        & (detail["top_n"] == 3)
        & (detail["holding_months"] == 1)
    ].copy()

    if sub.empty:
        return "_No latest selection data available._"

    latest = sub.sort_values("decision_date").tail(12).copy()

    cols = [
        "decision_month",
        "decision_date",
        "stock_1",
        "mom_1",
        "stock_1_return",
        "stock_2",
        "mom_2",
        "stock_2_return",
        "stock_3",
        "mom_3",
        "stock_3_return",
        "avg_momentum",
        "holding_return",
    ]

    latest = latest[cols]

    latest = latest.rename(
        columns={
            "decision_month": "Decision Month",
            "decision_date": "Decision Date",
            "stock_1": "Top 1",
            "mom_1": "Top 1 Momentum",
            "stock_1_return": "Top 1 Return",
            "stock_2": "Top 2",
            "mom_2": "Top 2 Momentum",
            "stock_2_return": "Top 2 Return",
            "stock_3": "Top 3",
            "mom_3": "Top 3 Momentum",
            "stock_3_return": "Top 3 Return",
            "avg_momentum": "Avg Momentum",
            "holding_return": "Portfolio Hold 1M Return",
        }
    )

    for col in latest.columns:
        if "Momentum" in col or "Return" in col:
            latest[col] = latest[col].map(fmt_pct)

    return df_to_markdown(latest)


def format_qqq_table(qqq: pd.DataFrame) -> str:
    if qqq.empty:
        return "_No QQQ benchmark data available._"

    q = qqq.drop(columns=[c for c in qqq.columns if c.endswith("Trades")], errors="ignore").copy()
    q = q.rename(columns={"year": "Year"})

    for col in q.columns:
        if col != "Year":
            q[col] = q[col].map(fmt_pct)

    return df_to_markdown(q)


def format_data_audit() -> str:
    parts = []

    try:
        cur = pd.read_csv(CURRENT_TICKERS_FILE)
        parts.append(f"- Current Nasdaq-100 tickers saved: **{cur['ticker'].nunique()}**")
    except Exception:
        parts.append("- Current Nasdaq-100 tickers saved: _not available; run update_data.py first._")

    try:
        changes = pd.read_csv(COMPONENT_CHANGES_FILE)
        parts.append(f"- Component-change rows saved: **{len(changes)}**")
    except Exception:
        parts.append("- Component-change rows saved: _not available; run update_data.py first._")

    return "\n".join(parts)


def window_section(
    window: int,
    yearly: pd.DataFrame,
    comp: pd.DataFrame,
    summary: pd.DataFrame,
    detail: pd.DataFrame,
) -> str:
    return f"""## {window}-Month Momentum Strategy

### Backtest Yearly Compounded Returns

The table below uses non-overlapping compounding paths starting from January. Hold 1M compounds monthly decisions Jan through Dec, Hold 2M compounds Jan/Mar/May/Jul/Sep/Nov decisions, and Hold 3M compounds Jan/Apr/Jul/Oct decisions. The current year is labelled YTD when it is incomplete.

{format_yearly_table(yearly, window)}

### Benchmark Comparison Summary vs QQQ

This table compares each strategy combination with QQQ using the same non-overlapping holding-period path.

{format_benchmark_comparison(comp, window)}

### Summary

{format_summary(summary, window)}

### Latest Top-3 Monthly Selections

This table follows the same compact display style as the previous project: it only shows the latest Top-3 monthly selections, their momentum values, and the realized 1M holding returns.

{format_latest_selection(detail, window)}

_Note: The ranking is still recomputed using the Nasdaq-100 universe effective at each decision date. Universe audit fields are kept in `output/momentum_grid_detail.csv`, but are intentionally omitted here to keep the README readable._
"""


def main() -> None:
    yearly = pd.read_csv(YEARLY_RETURNS_FILE)
    summary = pd.read_csv(SUMMARY_FILE)
    detail = pd.read_csv(DETAIL_FILE)

    qqq = pd.read_csv(BENCHMARK_YEARLY_FILE) if BENCHMARK_YEARLY_FILE.exists() else pd.DataFrame()
    comp = pd.read_csv(BENCHMARK_COMPARISON_FILE) if BENCHMARK_COMPARISON_FILE.exists() else pd.DataFrame()

    sections = "\n".join(window_section(w, yearly, comp, summary, detail) for w in MOMENTUM_WINDOWS)

    content = f"""# Nasdaq-100 Monthly Point-in-Time Momentum Grid Backtest

This project tests Nasdaq-100 average-momentum strategies using **monthly point-in-time Nasdaq-100 constituents**.

## Strategy Definition

- Monthly decision date: first available trading day of each calendar month.
- Universe: Nasdaq-100 constituents effective on that decision date, reconstructed from the current Wikipedia Nasdaq-100 list and the component-change table.
- Momentum: average of the previous N one-month returns, using month-start adjusted prices.
- Momentum windows tested: 3, 4, 5, 6, and 7 months.
- Portfolios tested: Top 1, Top 2, and Top 3 stocks by momentum.
- Holding periods tested: 1M, 2M, and 3M.
- Yearly returns use non-overlapping compounding paths.

## Universe Rule

At every decision date, the project reconstructs the Nasdaq-100 list that was effective at that date and recomputes the momentum ranking only inside that universe.

If a component change happens after a monthly decision date, that change is not used until the next monthly decision. For example, if the index changes on May 18, the May 1 decision still uses the May 1 universe, while the June 1 decision uses the updated universe.

Data source for constituents and component changes: `{WIKI_URL}`.

**Interpretation note.** This point-in-time version can differ from a static-current-universe backtest. If a stock was added to the Nasdaq-100 after a decision date, it is excluded from that month even if it has strong momentum. This avoids look-ahead bias, but it also means results will not exactly match older projects that used today’s Nasdaq-100 list for all historical months.

{format_data_audit()}

## QQQ Benchmark Yearly Compounded Returns

{format_qqq_table(qqq)}

{sections}

## How to Run

```bash
pip install -r requirements.txt
python run_all.py
