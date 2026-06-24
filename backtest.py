from __future__ import annotations

import pandas as pd

from config import (
    BACKTEST_START,
    BENCHMARK_COMPARISON_FILE,
    BENCHMARK_DETAIL_FILE,
    BENCHMARK_PRICE_FILE,
    BENCHMARK_TICKER,
    BENCHMARK_YEARLY_FILE,
    COMPONENT_CHANGES_FILE,
    CURRENT_TICKERS_FILE,
    DETAIL_FILE,
    HOLDING_MONTHS,
    MOMENTUM_WINDOWS,
    OUTPUT_DIR,
    PRICE_FILE,
    SUMMARY_FILE,
    TOP_NS,
    YEARLY_RETURNS_FILE,
)


def clean_ticker(value) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip().upper().replace(".", "-")
    return text if text and text not in {"NAN", "NONE", "—", "-"} else None


def get_month_start_prices(daily_prices: pd.DataFrame) -> pd.DataFrame:
    """Use the first available trading day of each month as the monthly anchor."""
    daily_prices = daily_prices.sort_index()
    groups = daily_prices.groupby(daily_prices.index.to_period("M"))
    first_rows = []
    first_dates = []
    for _, group in groups:
        if group.empty:
            continue
        first_rows.append(group.iloc[0])
        first_dates.append(group.index[0])
    out = pd.DataFrame(first_rows, index=pd.DatetimeIndex(first_dates))
    out.index.name = "decision_date"
    return out


def compute_momentum(month_start_prices: pd.DataFrame, window: int) -> pd.DataFrame:
    """Momentum = average of the previous N one-month returns.

    No extra shift is applied. At a month-start decision date, the latest completed
    month-start-to-month-start return is included, matching the first project.
    """
    monthly_returns = month_start_prices.pct_change(fill_method=None)
    return monthly_returns.rolling(window=window, min_periods=window).mean()


def load_current_tickers() -> set[str]:
    df = pd.read_csv(CURRENT_TICKERS_FILE)
    if "ticker" not in df.columns:
        raise ValueError(f"{CURRENT_TICKERS_FILE} must have column: ticker")
    return {t for t in df["ticker"].map(clean_ticker).dropna().tolist() if t}


def load_component_changes() -> pd.DataFrame:
    df = pd.read_csv(COMPONENT_CHANGES_FILE)
    if df.empty:
        return pd.DataFrame(columns=["date", "added_ticker", "removed_ticker"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["added_ticker"] = df.get("added_ticker", pd.Series(index=df.index, dtype=object)).map(clean_ticker)
    df["removed_ticker"] = df.get("removed_ticker", pd.Series(index=df.index, dtype=object)).map(clean_ticker)
    return df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)


def universe_as_of(decision_date: pd.Timestamp, current_tickers: set[str], changes: pd.DataFrame) -> set[str]:
    """Reconstruct Nasdaq-100 constituents effective at decision_date.

    Start from today's current list and reverse every component change whose date
    is after the decision date. A change on or before the decision date is already
    known and should remain reflected in the current-forward timeline.
    """
    membership = set(current_tickers)
    if changes.empty:
        return membership

    future_changes = changes[changes["date"] > decision_date].sort_values("date", ascending=False)
    for _, row in future_changes.iterrows():
        added = clean_ticker(row.get("added_ticker"))
        removed = clean_ticker(row.get("removed_ticker"))
        # Reverse a future change: later additions were not present yet;
        # later removals were still present then.
        if added:
            membership.discard(added)
        if removed:
            membership.add(removed)
    return membership


def non_overlap_months(holding_months: int) -> list[int]:
    if holding_months == 1:
        return list(range(1, 13))
    if holding_months == 2:
        return [1, 3, 5, 7, 9, 11]
    if holding_months == 3:
        return [1, 4, 7, 10]
    raise ValueError(f"Unsupported holding period: {holding_months}")


def run_window_backtest(
    month_start_prices: pd.DataFrame,
    current_tickers: set[str],
    changes: pd.DataFrame,
    window: int,
) -> pd.DataFrame:
    momentum = compute_momentum(month_start_prices, window)
    backtest_start = pd.Timestamp(BACKTEST_START)

    rows: list[dict] = []
    dates = list(month_start_prices.index)
    date_to_pos = {d: i for i, d in enumerate(dates)}

    for decision_date in dates:
        if decision_date < backtest_start:
            continue

        raw_universe = universe_as_of(decision_date, current_tickers, changes)
        universe = sorted(t for t in raw_universe if t in momentum.columns)
        if not universe:
            continue

        price_row = month_start_prices.loc[decision_date]
        valid = [t for t in universe if pd.notna(price_row.get(t, pd.NA))]
        if not valid:
            continue

        # Recompute the ranking at every decision date using the then-current universe.
        mom_row = momentum.loc[decision_date, valid].dropna().sort_values(ascending=False)
        if mom_row.empty:
            continue

        pos = date_to_pos[decision_date]

        for top_n in TOP_NS:
            selected = mom_row.head(top_n)
            if len(selected) < top_n:
                continue

            selected_tickers = selected.index.tolist()
            selected_mom = selected.values.tolist()
            avg_momentum = float(selected.mean())

            for hold_m in HOLDING_MONTHS:
                sell_pos = pos + hold_m
                if sell_pos >= len(dates):
                    continue

                sell_date = dates[sell_pos]
                buy_prices = month_start_prices.loc[decision_date, selected_tickers]
                sell_prices = month_start_prices.loc[sell_date, selected_tickers]
                stock_returns = (sell_prices / buy_prices - 1).dropna()

                if len(stock_returns) < top_n:
                    continue

                row = {
                    "decision_month": decision_date.strftime("%Y-%m"),
                    "decision_date": decision_date.strftime("%Y-%m-%d"),
                    "sell_date": sell_date.strftime("%Y-%m-%d"),
                    "universe_asof_date": decision_date.strftime("%Y-%m-%d"),
                    "raw_universe_size": len(raw_universe),
                    "available_universe_size": len(valid),
                    "momentum_window": window,
                    "holding_months": hold_m,
                    "top_n": top_n,
                    "avg_momentum": avg_momentum,
                    "holding_return": float(stock_returns.mean()),
                }
                for i in range(1, 4):
                    if i <= len(selected_tickers):
                        ticker = selected_tickers[i - 1]
                        row[f"stock_{i}"] = ticker
                        row[f"mom_{i}"] = float(selected_mom[i - 1])
                        row[f"stock_{i}_return"] = float(stock_returns.get(ticker, pd.NA))
                    else:
                        row[f"stock_{i}"] = ""
                        row[f"mom_{i}"] = pd.NA
                        row[f"stock_{i}_return"] = pd.NA
                rows.append(row)

    detail = pd.DataFrame(rows)
    if detail.empty:
        raise RuntimeError(f"No backtest results for {window}-month momentum window.")
    return detail


def build_yearly_returns(detail: pd.DataFrame) -> pd.DataFrame:
    df = detail.copy()
    df["decision_date"] = pd.to_datetime(df["decision_date"])
    df["year"] = df["decision_date"].dt.year
    df["month"] = df["decision_date"].dt.month

    rows: list[dict] = []
    for window in MOMENTUM_WINDOWS:
        for year in sorted(df["year"].dropna().unique()):
            row = {"momentum_window": window, "year": int(year)}
            for top_n in TOP_NS:
                for hold_m in HOLDING_MONTHS:
                    months = non_overlap_months(hold_m)
                    sub = df[
                        (df["momentum_window"] == window)
                        & (df["year"] == year)
                        & (df["top_n"] == top_n)
                        & (df["holding_months"] == hold_m)
                        & (df["month"].isin(months))
                    ].sort_values("decision_date")
                    row[f"Top {top_n} Hold {hold_m}M"] = pd.NA if sub.empty else float((1 + sub["holding_return"]).prod() - 1)
                    row[f"Top {top_n} Hold {hold_m}M Trades"] = int(len(sub))
            rows.append(row)

    result = pd.DataFrame(rows)
    result.to_csv(YEARLY_RETURNS_FILE, index=False)
    return result


def build_summary(detail: pd.DataFrame) -> pd.DataFrame:
    return (
        detail.groupby(["momentum_window", "top_n", "holding_months"], as_index=False)
        .agg(
            trades=("holding_return", "count"),
            avg_return=("holding_return", "mean"),
            median_return=("holding_return", "median"),
            win_rate=("holding_return", lambda x: (x > 0).mean()),
            best_return=("holding_return", "max"),
            worst_return=("holding_return", "min"),
            avg_available_universe_size=("available_universe_size", "mean"),
        )
        .sort_values(["momentum_window", "top_n", "holding_months"])
    )


def build_benchmark_detail(benchmark_month_start: pd.DataFrame) -> pd.DataFrame:
    benchmark_month_start = benchmark_month_start.sort_index()
    if BENCHMARK_TICKER in benchmark_month_start.columns:
        prices = benchmark_month_start[BENCHMARK_TICKER].dropna()
    else:
        prices = benchmark_month_start.iloc[:, 0].dropna()

    dates = list(prices.index)
    backtest_start = pd.Timestamp(BACKTEST_START)
    rows: list[dict] = []

    for pos, decision_date in enumerate(dates):
        if decision_date < backtest_start:
            continue
        for hold_m in HOLDING_MONTHS:
            sell_pos = pos + hold_m
            if sell_pos >= len(dates):
                continue
            sell_date = dates[sell_pos]
            rows.append(
                {
                    "decision_month": decision_date.strftime("%Y-%m"),
                    "decision_date": decision_date.strftime("%Y-%m-%d"),
                    "sell_date": sell_date.strftime("%Y-%m-%d"),
                    "holding_months": hold_m,
                    "benchmark_ticker": BENCHMARK_TICKER,
                    "benchmark_return": float(prices.loc[sell_date] / prices.loc[decision_date] - 1),
                }
            )
    return pd.DataFrame(rows)


def build_benchmark_yearly(benchmark_detail: pd.DataFrame) -> pd.DataFrame:
    if benchmark_detail.empty:
        return pd.DataFrame()
    df = benchmark_detail.copy()
    df["decision_date"] = pd.to_datetime(df["decision_date"])
    df["year"] = df["decision_date"].dt.year
    rows: list[dict] = []
    for year in sorted(df["year"].dropna().unique()):
        year_df = df[df["year"] == year].copy()
        row = {"year": int(year)}
        for hold_m in HOLDING_MONTHS:
            months = non_overlap_months(hold_m)
            sub = year_df[
                (year_df["holding_months"] == hold_m)
                & (year_df["decision_date"].dt.month.isin(months))
            ].sort_values("decision_date")
            row[f"QQQ Hold {hold_m}M"] = pd.NA if sub.empty else float((1 + sub["benchmark_return"]).prod() - 1)
            row[f"QQQ Hold {hold_m}M Trades"] = int(len(sub))
        rows.append(row)
    result = pd.DataFrame(rows)
    result.to_csv(BENCHMARK_YEARLY_FILE, index=False)
    return result


def build_benchmark_comparison(yearly: pd.DataFrame, qqq: pd.DataFrame) -> pd.DataFrame:
    if yearly.empty or qqq.empty:
        return pd.DataFrame()
    merged = yearly.merge(qqq, on="year", how="left")
    rows = []
    for window in MOMENTUM_WINDOWS:
        subw = merged[merged["momentum_window"] == window]
        for top_n in TOP_NS:
            for hold_m in HOLDING_MONTHS:
                scol = f"Top {top_n} Hold {hold_m}M"
                bcol = f"QQQ Hold {hold_m}M"
                valid = subw[[scol, bcol]].dropna()
                if valid.empty:
                    years = 0
                    avg_strategy = avg_qqq = avg_excess = beat_rate = best_excess = worst_excess = pd.NA
                else:
                    excess = valid[scol] - valid[bcol]
                    years = int(len(valid))
                    avg_strategy = float(valid[scol].mean())
                    avg_qqq = float(valid[bcol].mean())
                    avg_excess = float(excess.mean())
                    beat_rate = float((excess > 0).mean())
                    best_excess = float(excess.max())
                    worst_excess = float(excess.min())
                rows.append(
                    {
                        "momentum_window": window,
                        "top_n": top_n,
                        "holding_months": hold_m,
                        "years": years,
                        "avg_strategy_yearly_return": avg_strategy,
                        "avg_qqq_yearly_return": avg_qqq,
                        "avg_excess_return": avg_excess,
                        "beat_rate_vs_qqq": beat_rate,
                        "best_excess": best_excess,
                        "worst_excess": worst_excess,
                    }
                )
    result = pd.DataFrame(rows)
    result.to_csv(BENCHMARK_COMPARISON_FILE, index=False)
    return result


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    daily_prices = pd.read_csv(PRICE_FILE, index_col="date", parse_dates=True).sort_index()
    month_prices = get_month_start_prices(daily_prices)
    current_tickers = load_current_tickers()
    changes = load_component_changes()

    benchmark_daily = pd.read_csv(BENCHMARK_PRICE_FILE, index_col="date", parse_dates=True).sort_index()
    benchmark_month_start = get_month_start_prices(benchmark_daily)
    benchmark_detail = build_benchmark_detail(benchmark_month_start)
    benchmark_yearly = build_benchmark_yearly(benchmark_detail)
    benchmark_detail.to_csv(BENCHMARK_DETAIL_FILE, index=False)

    all_details = []
    for window in MOMENTUM_WINDOWS:
        detail = run_window_backtest(month_prices, current_tickers, changes, window)
        all_details.append(detail)
        per_window_file = OUTPUT_DIR / f"momentum_{window}m_detail.csv"
        detail.to_csv(per_window_file, index=False)
        print(f"Saved {per_window_file}")

    full_detail = pd.concat(all_details, ignore_index=True)
    full_detail.to_csv(DETAIL_FILE, index=False)
    print(f"Saved {DETAIL_FILE}")

    summary = build_summary(full_detail)
    summary.to_csv(SUMMARY_FILE, index=False)
    print(f"Saved {SUMMARY_FILE}")

    yearly = build_yearly_returns(full_detail)
    print(f"Saved {YEARLY_RETURNS_FILE}")

    build_benchmark_comparison(yearly, benchmark_yearly)
    print(f"Saved {BENCHMARK_COMPARISON_FILE}")


if __name__ == "__main__":
    main()
