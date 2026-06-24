from pathlib import Path

code = r'''from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from config import (
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
    sub["Year"] = sub["Year"].apply(
        lambda y: f"{int(y)} (YTD)" if y == current_year else int(y)
    )

    return df_to_markdown(sub)


def format_summary(summary: pd.DataFrame, window: int) -> str:
    sub = summary[summary["momentum_window"] == window].copy()

    if sub.empty:
        return "_No summary data available._"

    sub = sub.drop(columns=["avg_available_universe_size"], errors="ignore")

    sub = sub.rename(
        columns={
            "momentum_window": "Momentum Window",
            "top_n": "Top N",
            "holding_months": "Holding Months",
            "trades": "Trades",
            "avg_return": "Avg Return",
            "median_return": "Median Return",
            "win_rate": "Win Rate",
            "best_return": "Best Return",
            "worst_return": "Worst Return",
        }
    )

    ordered_cols = [
        "Momentum Window",
        "Top N",
        "Holding Months",
        "Trades",
        "Avg Return",
        "Median Return",
        "Win Rate",
        "Best Return",
        "Worst Return",
    ]
    sub = sub[[c for c in ordered_cols if c in sub.columns]]

    for col in ["Avg Return", "Median Return", "Win Rate", "Best Return", "Worst Return"]:
        if col in sub.columns:
            sub[col] = sub[col].map(fmt_pct)

    return df_to_markdown(sub)


def format_benchmark_comparison(comp: pd.DataFrame, window: int) -> str:
    sub = comp[comp["momentum_window"] == window].copy()

    if sub.empty:
        return "_No benchmark comparison available._"

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
    """
    Show the latest Top-3 ranking components.

    Top 1 / Top 2 / Top 3 are the rank-1, rank-2, rank-3 stocks
    in the monthly momentum ranking.

    For each ranked stock, this table shows the realized 1M / 2M / 3M
    individual stock returns from the same decision date.
    """
    sub = detail[
        (detail["momentum_window"] == window)
        & (detail["top_n"] == 3)
        & (detail["holding_months"].isin([1, 2, 3]))
    ].copy()

    if sub.empty:
        return "_No latest selection data available._"

    key_cols = ["decision_month", "decision_date"]

    # Use 1M rows as the base because the ranking/momentum fields are identical
    # across 1M, 2M, and 3M holding-period variants for the same decision date.
    base = (
        sub[sub["holding_months"] == 1]
        .sort_values("decision_date")
        .tail(12)
        .copy()
    )

    if base.empty:
        return "_No latest selection data available._"

    base = base[
        key_cols
        + [
            "stock_1",
            "mom_1",
            "stock_2",
            "mom_2",
            "stock_3",
            "mom_3",
            "avg_momentum",
        ]
    ].copy()

    # Merge individual stock returns for 1M, 2M, and 3M holding periods.
    for h in [1, 2, 3]:
        ret = sub[sub["holding_months"] == h][
            key_cols
            + [
                "stock_1_return",
                "stock_2_return",
                "stock_3_return",
            ]
        ].copy()

        ret = ret.rename(
            columns={
                "stock_1_return": f"Top 1 {h}M Return",
                "stock_2_return": f"Top 2 {h}M Return",
                "stock_3_return": f"Top 3 {h}M Return",
            }
        )

        base = base.merge(ret, on=key_cols, how="left")

    latest = base.rename(
        columns={
            "decision_month": "Decision Month",
            "decision_date": "Decision Date",
            "stock_1": "Top 1",
            "mom_1": "Top 1 Momentum",
            "stock_2": "Top 2",
            "mom_2": "Top 2 Momentum",
            "stock_3": "Top 3",
            "mom_3": "Top 3 Momentum",
            "avg_momentum": "Avg Momentum",
        }
    )

    ordered_cols = [
        "Decision Month",
        "Decision Date",
        "Top 1",
        "Top 1 Momentum",
        "Top 1 1M Return",
        "Top 1 2M Return",
        "Top 1 3M Return",
        "Top 2",
        "Top 2 Momentum",
        "Top 2 1M Return",
        "Top 2 2M Return",
        "Top 2 3M Return",
        "Top 3",
        "Top 3 Momentum",
        "Top 3 1M Return",
        "Top 3 2M Return",
        "Top 3 3M Return",
        "Avg Momentum",
    ]

    latest = latest[[c for c in ordered_cols if c in latest.columns]]

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
    parts = [
        f"## {window}-Month Momentum Strategy",
        "",
        "### Backtest Yearly Compounded Returns",
        "",
        (
            "The table below uses non-overlapping compounding paths starting from January.\n"
            "Hold 1M compounds monthly decisions Jan through Dec, "
            "Hold 2M compounds Jan/Mar/May/Jul/Sep/Nov decisions, and "
            "Hold 3M compounds Jan/Apr/Jul/Oct decisions.\n"
            "The current year is labelled YTD when it is incomplete."
        ),
        "",
        format_yearly_table(yearly, window),
        "",
        "### Benchmark Comparison Summary vs QQQ",
        "",
        "This table compares each strategy combination with QQQ using the same non-overlapping holding-period path.",
        "",
        format_benchmark_comparison(comp, window),
        "",
        "### Summary",
        "",
        format_summary(summary, window),
        "",
        "### Latest Top-3 Monthly Selections",
        "",
        (
            "This table shows the latest Top-3 monthly selections, their momentum values, "
            "and the realized 1M / 2M / 3M holding returns for each selected stock."
        ),
        "",
        format_latest_selection(detail, window),
        "",
        (
            "_Note: The ranking is still recomputed using the Nasdaq-100 universe effective "
            "at each decision date. Universe audit fields are kept in "
            "`output/momentum_grid_detail.csv`, but are intentionally omitted here to keep "
            "the README readable._"
        ),
        "",
    ]

    return "\n".join(parts)


def main() -> None:
    yearly = pd.read_csv(YEARLY_RETURNS_FILE)
    summary = pd.read_csv(SUMMARY_FILE)
    detail = pd.read_csv(DETAIL_FILE)

    qqq = pd.read_csv(BENCHMARK_YEARLY_FILE) if BENCHMARK_YEARLY_FILE.exists() else pd.DataFrame()
    comp = (
        pd.read_csv(BENCHMARK_COMPARISON_FILE)
        if BENCHMARK_COMPARISON_FILE.exists()
        else pd.DataFrame()
    )

    sections = "\n".join(
        window_section(w, yearly, comp, summary, detail)
        for w in MOMENTUM_WINDOWS
    )

    content_parts = [
        "# Nasdaq-100 Point-in-Time Momentum Grid Backtest vs QQQ",
        "",
        "This project compares Nasdaq-100 average-momentum strategies using five momentum windows:",
        "",
        "- 3-month average momentum",
        "- 4-month average momentum",
        "- 5-month average momentum",
        "- 6-month average momentum",
        "- 7-month average momentum",
        "",
        "For each momentum window, the project tests:",
        "",
        "- Top 1 / Top 2 / Top 3 selected stocks",
        "- 1 / 2 / 3 month holding periods",
        "- Monthly decisions from 2016 to the latest available completed holding period",
        "",
        (
            "The README is automatically regenerated from the CSV outputs. "
            "For each momentum window, the README shows:"
        ),
        "",
        "1. Backtest Yearly Compounded Returns",
        "2. Benchmark Comparison Summary vs QQQ",
        "3. Summary",
        "4. Latest Top-3 Monthly Selections",
        "",
        "The full monthly decision-level data is saved in `output/momentum_grid_detail.csv`.",
        "",
        f"Last updated: **{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "## Method",
        "",
        "- Stock universe: monthly point-in-time Nasdaq-100 constituents",
        "- Decision date: first available trading day of each month",
        "- Momentum definition: average of the previous N one-month returns based on month-start adjusted close prices",
        "- Momentum windows: 3 / 4 / 5 / 6 / 7 months",
        "- Buy price: adjusted close on the decision date",
        "- Sell price: adjusted close on the first trading day after the selected holding period",
        "- Portfolio return: equal-weighted average return of the selected stocks",
        "- Yearly compounded return: non-overlapping compounding path starting from January",
        "",
        "## Universe Rule",
        "",
        (
            "At every decision date, the project reconstructs the Nasdaq-100 list that was "
            "effective at that date and recomputes the momentum ranking only inside that universe."
        ),
        "",
        (
            "If a component change happens after a monthly decision date, that change is not used "
            "until the next monthly decision. For example, if the index changes on May 18, "
            "the May 1 decision still uses the May 1 universe, while the June 1 decision uses "
            "the updated universe."
        ),
        "",
        f"Data source for constituents and component changes: `{WIKI_URL}`.",
        "",
        (
            "**Interpretation note.** This point-in-time version can differ from a static-current-universe "
            "backtest. If a stock was added to the Nasdaq-100 after a decision date, it is excluded "
            "from that month even if it has strong momentum. This avoids look-ahead bias, but it also "
            "means results will not exactly match older projects that used today’s Nasdaq-100 list for "
            "all historical months."
        ),
        "",
        format_data_audit(),
        "",
        "## QQQ Benchmark Yearly Compounded Returns",
        "",
        format_qqq_table(qqq),
        "",
        sections,
        "",
        "## How to Run",
        "",
        "```bash",
        "pip install -r requirements.txt",
        "python run_all.py",
        "```",
        "",
        "Generated outputs are saved in `output/`.",
        "",
        "Important output files:",
        "",
        "- `data/nasdaq100_current_tickers.csv`: current Nasdaq-100 list downloaded from Wikipedia.",
        "- `data/nasdaq100_component_changes.csv`: component changes parsed from Wikipedia.",
        "- `data/nasdaq100_all_historical_tickers.csv`: all current, added, and removed tickers used for price downloads.",
        "- `output/momentum_grid_detail.csv`: full monthly selections, effective universe date, selected stocks, momentum, and holding returns.",
        "- `output/yearly_compounded_returns.csv`: annual compounded return table for all 3/4/5/6/7-month momentum windows.",
        "- `output/momentum_grid_summary.csv`: strategy summary statistics.",
        "- `output/benchmark_comparison_summary.csv`: QQQ comparison summary.",
        "",
    ]

    content = "\n".join(content_parts)
    README_FILE.write_text(content, encoding="utf-8")

    print(f"Updated {README_FILE}")


if __name__ == "__main__":
    main()
'''

path = Path("/mnt/data/update_readme.py")
path.write_text(code, encoding="utf-8")
print(path)
