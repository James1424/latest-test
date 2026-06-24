def format_latest_selection(detail: pd.DataFrame, window: int) -> str:
    sub = detail[
        (detail["momentum_window"] == window)
        & (detail["top_n"] == 3)
        & (detail["holding_months"].isin([1, 2, 3]))
    ].copy()

    if sub.empty:
        return "_No latest selection data available._"

    key_cols = ["decision_month", "decision_date"]

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

    # Add stock-level realized returns for 1M / 2M / 3M holding periods.
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
