# Nasdaq-100 Monthly Point-in-Time Momentum Grid Backtest

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

Data source for constituents and component changes: `https://en.wikipedia.org/wiki/Nasdaq-100`.

**Interpretation note.** This point-in-time version can differ from a static-current-universe backtest. If a stock was added to the Nasdaq-100 after a decision date, it is excluded from that month even if it has strong momentum. This avoids look-ahead bias, but it also means results will not exactly match older projects that used today’s Nasdaq-100 list for all historical months.

- Current Nasdaq-100 tickers saved: **101**
- Component-change rows saved: **225**

## QQQ Benchmark Yearly Compounded Returns

|   Year | QQQ Hold 1M   | QQQ Hold 2M   | QQQ Hold 3M   |
|-------:|:--------------|:--------------|:--------------|
|   2016 | 10.38%        | 10.38%        | 10.38%        |
|   2017 | 33.79%        | 33.79%        | 33.79%        |
|   2018 | -1.45%        | -1.45%        | -1.45%        |
|   2019 | 40.72%        | 40.72%        | 40.72%        |
|   2020 | 43.91%        | 43.91%        | 43.91%        |
|   2021 | 30.49%        | 30.49%        | 30.49%        |
|   2022 | -33.67%       | -33.67%       | -33.67%       |
|   2023 | 53.27%        | 53.27%        | 53.27%        |
|   2024 | 27.49%        | 27.49%        | 27.49%        |
|   2025 | 20.77%        | 20.77%        | 20.77%        |
|   2026 | 21.29%        | 10.09%        | -4.58%        |

## 3-Month Momentum Strategy

### Backtest Yearly Compounded Returns

The table below uses non-overlapping compounding paths starting from January. Hold 1M compounds monthly decisions Jan through Dec, Hold 2M compounds Jan/Mar/May/Jul/Sep/Nov decisions, and Hold 3M compounds Jan/Apr/Jul/Oct decisions. The current year is labelled YTD when it is incomplete.

| Year       | Top 1 Hold 1M   | Top 1 Hold 2M   | Top 1 Hold 3M   | Top 2 Hold 1M   | Top 2 Hold 2M   | Top 2 Hold 3M   | Top 3 Hold 1M   | Top 3 Hold 2M   | Top 3 Hold 3M   |
|:-----------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|
| 2016       | 57.85%          | 29.82%          | 65.50%          | 18.12%          | 10.29%          | 41.70%          | 18.06%          | 4.61%           | 47.48%          |
| 2017       | 10.20%          | 3.61%           | 59.12%          | 36.48%          | 13.47%          | 59.86%          | 32.79%          | 17.21%          | 37.77%          |
| 2018       | 8.70%           | 12.42%          | 4.13%           | -27.63%         | -11.10%         | -16.62%         | -5.74%          | -2.75%          | -0.91%          |
| 2019       | -7.04%          | 12.87%          | 57.13%          | 38.42%          | 41.42%          | 55.36%          | 60.65%          | 53.62%          | 48.54%          |
| 2020       | 187.78%         | 333.27%         | 748.06%         | 217.76%         | 189.74%         | 232.58%         | 233.64%         | 182.97%         | 132.24%         |
| 2021       | 37.41%          | 14.60%          | -15.75%         | 46.42%          | 44.67%          | -1.15%          | 54.55%          | 43.42%          | -2.04%          |
| 2022       | -64.55%         | -54.27%         | -40.71%         | -50.85%         | -36.70%         | -37.57%         | -38.66%         | -40.48%         | -28.47%         |
| 2023       | 29.40%          | -13.11%         | 75.90%          | 55.34%          | 38.87%          | 65.11%          | 26.53%          | 44.68%          | 46.04%          |
| 2024       | -38.20%         | -18.26%         | -3.07%          | -3.39%          | -5.60%          | 19.36%          | 8.56%           | 13.07%          | 24.35%          |
| 2025       | 11.81%          | 274.61%         | -20.89%         | 21.28%          | 149.46%         | 35.71%          | 4.95%           | 81.44%          | 26.23%          |
| 2026 (YTD) | 85.58%          | 71.97%          | 16.67%          | 131.79%         | 60.00%          | 5.37%           | 134.23%         | 42.99%          | 2.39%           |

### Benchmark Comparison Summary vs QQQ

This table compares each strategy combination with QQQ using the same non-overlapping holding-period path.

|   Top N |   Holding Months |   Years | Avg Strategy Yearly Return   | Avg QQQ Yearly Return   | Avg Excess Return   | Beat Rate vs QQQ   | Best Excess   | Worst Excess   |
|--------:|-----------------:|--------:|:-----------------------------|:------------------------|:--------------------|:-------------------|:--------------|:---------------|
|       1 |                1 |      11 | 28.99%                       | 22.45%                  | 6.54%               | 45.45%             | 143.87%       | -65.69%        |
|       1 |                2 |      11 | 60.69%                       | 21.44%                  | 39.25%              | 45.45%             | 289.36%       | -66.38%        |
|       1 |                3 |      11 | 86.01%                       | 20.10%                  | 65.91%              | 63.64%             | 704.15%       | -46.24%        |
|       2 |                1 |      11 | 43.98%                       | 22.45%                  | 21.52%              | 63.64%             | 173.85%       | -30.88%        |
|       2 |                2 |      11 | 44.96%                       | 21.44%                  | 23.52%              | 45.45%             | 145.83%       | -33.09%        |
|       2 |                3 |      11 | 41.79%                       | 20.10%                  | 21.69%              | 63.64%             | 188.67%       | -31.64%        |
|       3 |                1 |      11 | 48.14%                       | 22.45%                  | 25.69%              | 45.45%             | 189.74%       | -26.74%        |
|       3 |                2 |      11 | 40.07%                       | 21.44%                  | 18.64%              | 45.45%             | 139.06%       | -16.58%        |
|       3 |                3 |      11 | 30.33%                       | 20.10%                  | 10.23%              | 72.73%             | 88.33%        | -32.53%        |

### Summary

|   Top N |   Holding Months |   Trades | Avg Return   | Median Return   | Win Rate   | Best Return   | Worst Return   |   Avg Available Universe |
|--------:|-----------------:|---------:|:-------------|:----------------|:-----------|:--------------|:---------------|-------------------------:|
|       1 |                1 |      125 | 2.26%        | 0.35%           | 51.20%     | 81.29%        | -35.24%        |                     92.2 |
|       1 |                2 |      123 | 7.35%        | 1.22%           | 54.47%     | 112.15%       | -38.94%        |                     92.2 |
|       1 |                3 |      122 | 12.94%       | 6.08%           | 54.10%     | 151.03%       | -50.66%        |                     92.1 |
|       2 |                1 |      125 | 2.95%        | 0.69%           | 53.60%     | 58.37%        | -24.59%        |                     92.2 |
|       2 |                2 |      123 | 6.94%        | 2.59%           | 56.91%     | 100.59%       | -33.45%        |                     92.2 |
|       2 |                3 |      122 | 10.00%       | 5.20%           | 68.85%     | 126.68%       | -28.37%        |                     92.1 |
|       3 |                1 |      125 | 3.19%        | 0.81%           | 56.00%     | 50.97%        | -22.72%        |                     92.2 |
|       3 |                2 |      123 | 6.65%        | 3.43%           | 62.60%     | 121.61%       | -31.41%        |                     92.2 |
|       3 |                3 |      122 | 8.80%        | 4.76%           | 72.13%     | 96.94%        | -29.19%        |                     92.1 |

### Latest Top-3 Monthly Selections

This table follows the same compact display style as the previous project: it only shows the latest Top-3 monthly selections, their momentum values, and the realized 1M holding returns.

| Decision Month   | Decision Date   | Top 1   | Top 1 Momentum   | Top 1 Return   | Top 2   | Top 2 Momentum   | Top 2 Return   | Top 3   | Top 3 Momentum   | Top 3 Return   | Avg Momentum   | Portfolio Hold 1M Return   |
|:-----------------|:----------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:---------------|:---------------------------|
| 2025-06          | 2025-06-02      | PLTR    | 17.45%           | -1.03%         | ZS      | 16.18%           | 4.82%          | MSTR    | 14.74%           | 0.28%          | 16.13%         | 1.36%                      |
| 2025-07          | 2025-07-01      | AVGO    | 16.61%           | 9.03%          | PLTR    | 16.61%           | 18.05%         | ZS      | 15.62%           | -8.80%         | 16.28%         | 6.09%                      |
| 2025-08          | 2025-08-01      | AMD     | 21.16%           | -5.46%         | TTD     | 18.78%           | -37.06%        | NVDA    | 16.00%           | -1.69%         | 18.65%         | -14.74%                    |
| 2025-09          | 2025-09-02      | AMD     | 13.14%           | 1.04%          | SHOP    | 9.42%            | 7.57%          | SNPS    | 8.73%            | -17.44%        | 10.43%         | -2.94%                     |
| 2025-10          | 2025-10-01      | APP     | 28.61%           | -10.22%        | WBD     | 24.82%           | 15.19%         | INTC    | 19.44%           | 9.91%          | 24.29%         | 4.96%                      |
| 2025-11          | 2025-11-03      | MU      | 31.88%           | 2.45%          | INTC    | 27.91%           | 1.29%          | WBD     | 24.00%           | 7.09%          | 27.93%         | 3.61%                      |
| 2025-12          | 2025-12-01      | WBD     | 29.60%           | 19.44%         | MU      | 28.37%           | 31.23%         | INTC    | 19.88%           | -1.57%         | 25.95%         | 16.36%                     |
| 2026-01          | 2026-01-02      | MU      | 20.87%           | 38.80%         | AMD     | 14.88%           | 10.20%         | WBD     | 13.91%           | -3.47%         | 16.55%         | 15.18%                     |
| 2026-02          | 2026-02-02      | MU      | 24.16%           | -5.74%         | WDC     | 20.78%           | -0.06%         | STX     | 19.67%           | -12.34%        | 21.54%         | -6.05%                     |
| 2026-03          | 2026-03-02      | MU      | 21.43%           | -10.82%        | WDC     | 19.59%           | 10.29%         | LRCX    | 15.12%           | -3.78%         | 18.71%         | -1.44%                     |
| 2026-04          | 2026-04-01      | WDC     | 18.07%           | 44.94%         | STX     | 16.64%           | 71.80%         | ARM     | 11.40%           | 36.18%         | 15.37%         | 50.97%                     |
| 2026-05          | 2026-05-01      | INTC    | 35.40%           | 9.75%          | MRVL    | 29.81%           | 33.03%         | ARM     | 25.73%           | 93.60%         | 30.31%         | 45.46%                     |

_Note: The ranking is still recomputed using the Nasdaq-100 universe effective at each decision date. Universe audit fields are kept in `output/momentum_grid_detail.csv`, but are intentionally omitted here to keep the README readable._

## 4-Month Momentum Strategy

### Backtest Yearly Compounded Returns

The table below uses non-overlapping compounding paths starting from January. Hold 1M compounds monthly decisions Jan through Dec, Hold 2M compounds Jan/Mar/May/Jul/Sep/Nov decisions, and Hold 3M compounds Jan/Apr/Jul/Oct decisions. The current year is labelled YTD when it is incomplete.

| Year       | Top 1 Hold 1M   | Top 1 Hold 2M   | Top 1 Hold 3M   | Top 2 Hold 1M   | Top 2 Hold 2M   | Top 2 Hold 3M   | Top 3 Hold 1M   | Top 3 Hold 2M   | Top 3 Hold 3M   |
|:-----------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|
| 2016       | 70.40%          | 67.94%          | 42.42%          | 72.92%          | 53.79%          | 52.85%          | 71.07%          | 50.69%          | 50.00%          |
| 2017       | 34.87%          | 65.10%          | 45.41%          | 24.04%          | 38.57%          | 37.98%          | 26.54%          | 34.21%          | 50.33%          |
| 2018       | 30.55%          | -4.43%          | 78.54%          | 29.50%          | -2.49%          | 28.90%          | 23.76%          | 2.27%           | 20.87%          |
| 2019       | 54.76%          | 40.46%          | 10.51%          | 21.04%          | 13.49%          | 30.70%          | 30.76%          | 9.55%           | 48.73%          |
| 2020       | 378.18%         | 728.89%         | 689.80%         | 246.57%         | 355.80%         | 194.48%         | 139.70%         | 254.32%         | 157.77%         |
| 2021       | 56.10%          | 199.57%         | 8.76%           | 8.14%           | 73.52%          | -4.93%          | 6.17%           | 39.25%          | -2.37%          |
| 2022       | -46.95%         | -44.08%         | -15.56%         | -38.60%         | -33.81%         | -11.29%         | -30.72%         | -12.63%         | 14.82%          |
| 2023       | 93.83%          | 70.81%          | 108.04%         | 83.60%          | 71.78%          | 81.04%          | 63.67%          | 89.92%          | 46.51%          |
| 2024       | 87.56%          | 109.68%         | 146.41%         | 22.90%          | -0.39%          | 30.64%          | 33.67%          | 5.98%           | 20.41%          |
| 2025       | 180.46%         | 37.91%          | 86.36%          | 99.20%          | 113.06%         | 114.38%         | 98.22%          | 124.40%         | 78.82%          |
| 2026 (YTD) | 150.93%         | 71.97%          | 16.67%          | 132.92%         | 68.08%          | 6.55%           | 131.47%         | 64.79%          | 23.93%          |

### Benchmark Comparison Summary vs QQQ

This table compares each strategy combination with QQQ using the same non-overlapping holding-period path.

|   Top N |   Holding Months |   Years | Avg Strategy Yearly Return   | Avg QQQ Yearly Return   | Avg Excess Return   | Beat Rate vs QQQ   | Best Excess   | Worst Excess   |
|--------:|-----------------:|--------:|:-----------------------------|:------------------------|:--------------------|:-------------------|:--------------|:---------------|
|       1 |                1 |      11 | 99.15%                       | 22.45%                  | 76.70%              | 90.91%             | 334.27%       | -13.27%        |
|       1 |                2 |      11 | 122.17%                      | 21.44%                  | 100.73%             | 72.73%             | 684.98%       | -10.41%        |
|       1 |                3 |      11 | 110.67%                      | 20.10%                  | 90.57%              | 81.82%             | 645.89%       | -30.20%        |
|       2 |                1 |      11 | 63.84%                       | 22.45%                  | 41.39%              | 54.55%             | 202.67%       | -22.35%        |
|       2 |                2 |      11 | 68.31%                       | 21.44%                  | 46.87%              | 63.64%             | 311.89%       | -27.88%        |
|       2 |                3 |      11 | 51.03%                       | 20.10%                  | 30.93%              | 81.82%             | 150.57%       | -35.42%        |
|       3 |                1 |      11 | 54.03%                       | 22.45%                  | 31.57%              | 72.73%             | 110.18%       | -24.32%        |
|       3 |                2 |      11 | 60.25%                       | 21.44%                  | 38.81%              | 81.82%             | 210.41%       | -31.17%        |
|       3 |                3 |      11 | 46.35%                       | 20.10%                  | 26.24%              | 72.73%             | 113.86%       | -32.86%        |

### Summary

|   Top N |   Holding Months |   Trades | Avg Return   | Median Return   | Win Rate   | Best Return   | Worst Return   |   Avg Available Universe |
|--------:|-----------------:|---------:|:-------------|:----------------|:-----------|:--------------|:---------------|-------------------------:|
|       1 |                1 |      125 | 6.63%        | 3.42%           | 58.40%     | 81.29%        | -35.24%        |                     92.2 |
|       1 |                2 |      123 | 13.59%       | 9.63%           | 65.85%     | 132.93%       | -40.06%        |                     92.2 |
|       1 |                3 |      122 | 18.35%       | 15.15%          | 68.85%     | 151.03%       | -40.02%        |                     92.1 |
|       2 |                1 |      124 | 4.29%        | 2.67%           | 62.10%     | 58.37%        | -24.59%        |                     92.2 |
|       2 |                2 |      122 | 9.12%        | 6.85%           | 66.39%     | 100.59%       | -33.45%        |                     92.2 |
|       2 |                3 |      121 | 12.28%       | 6.55%           | 76.03%     | 126.68%       | -27.01%        |                     92.1 |
|       3 |                1 |      124 | 3.93%        | 1.88%           | 58.06%     | 54.71%        | -21.38%        |                     92.2 |
|       3 |                2 |      122 | 8.48%        | 5.30%           | 67.21%     | 127.56%       | -25.13%        |                     92.2 |
|       3 |                3 |      121 | 11.56%       | 7.80%           | 73.55%     | 92.21%        | -33.11%        |                     92.1 |

### Latest Top-3 Monthly Selections

This table follows the same compact display style as the previous project: it only shows the latest Top-3 monthly selections, their momentum values, and the realized 1M holding returns.

| Decision Month   | Decision Date   | Top 1   | Top 1 Momentum   | Top 1 Return   | Top 2   | Top 2 Momentum   | Top 2 Return   | Top 3   | Top 3 Momentum   | Top 3 Return   | Avg Momentum   | Portfolio Hold 1M Return   |
|:-----------------|:----------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:---------------|:---------------------------|
| 2025-06          | 2025-06-02      | PLTR    | 13.00%           | -1.03%         | ZS      | 10.74%           | 4.82%          | MELI    | 8.45%            | -3.55%         | 10.73%         | 0.08%                      |
| 2025-07          | 2025-07-01      | ZS      | 13.34%           | -8.80%         | PLTR    | 12.83%           | 18.05%         | MSTR    | 11.12%           | -1.79%         | 12.43%         | 2.49%                      |
| 2025-08          | 2025-08-01      | PLTR    | 16.97%           | 1.83%          | AVGO    | 14.71%           | 3.33%          | AMD     | 14.38%           | -5.46%         | 15.35%         | -0.10%                     |
| 2025-09          | 2025-09-02      | APP     | 16.81%           | 46.16%         | AMD     | 14.51%           | 1.04%          | MU      | 12.30%           | 53.74%         | 14.54%         | 33.65%                     |
| 2025-10          | 2025-10-01      | WBD     | 20.96%           | 15.19%         | MU      | 19.17%           | 28.93%         | INTC    | 18.52%           | 9.91%          | 19.55%         | 18.01%                     |
| 2025-11          | 2025-11-03      | WBD     | 22.41%           | 7.09%          | MU      | 20.62%           | 2.45%          | AMD     | 20.01%           | -15.36%        | 21.01%         | -1.94%                     |
| 2025-12          | 2025-12-01      | MU      | 24.52%           | 31.23%         | INTC    | 21.26%           | -1.57%         | WBD     | 19.77%           | 19.44%         | 21.85%         | 16.36%                     |
| 2026-01          | 2026-01-02      | MU      | 29.09%           | 38.80%         | WBD     | 27.06%           | -3.47%         | WDC     | 24.74%           | 43.97%         | 26.96%         | 26.43%                     |
| 2026-02          | 2026-02-02      | MU      | 25.35%           | -5.74%         | WDC     | 20.83%           | -0.06%         | STX     | 15.60%           | -12.34%        | 20.60%         | -6.05%                     |
| 2026-03          | 2026-03-02      | MU      | 16.68%           | -10.82%        | WDC     | 15.57%           | 10.29%         | AMAT    | 12.13%           | -4.94%         | 14.80%         | -1.82%                     |
| 2026-04          | 2026-04-01      | WDC     | 17.27%           | 44.94%         | STX     | 14.16%           | 71.80%         | MU      | 13.37%           | 47.40%         | 14.93%         | 54.71%                     |
| 2026-05          | 2026-05-01      | SNDK    | 54.50%           | 48.39%         | INTC    | 32.53%           | 9.75%          | STX     | 30.43%           | 26.73%         | 39.15%         | 28.29%                     |

_Note: The ranking is still recomputed using the Nasdaq-100 universe effective at each decision date. Universe audit fields are kept in `output/momentum_grid_detail.csv`, but are intentionally omitted here to keep the README readable._

## 5-Month Momentum Strategy

### Backtest Yearly Compounded Returns

The table below uses non-overlapping compounding paths starting from January. Hold 1M compounds monthly decisions Jan through Dec, Hold 2M compounds Jan/Mar/May/Jul/Sep/Nov decisions, and Hold 3M compounds Jan/Apr/Jul/Oct decisions. The current year is labelled YTD when it is incomplete.

| Year       | Top 1 Hold 1M   | Top 1 Hold 2M   | Top 1 Hold 3M   | Top 2 Hold 1M   | Top 2 Hold 2M   | Top 2 Hold 3M   | Top 3 Hold 1M   | Top 3 Hold 2M   | Top 3 Hold 3M   |
|:-----------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|
| 2016       | 52.68%          | 78.01%          | 61.02%          | 49.91%          | 75.78%          | 67.81%          | 52.97%          | 65.04%          | 66.94%          |
| 2017       | 47.53%          | 69.64%          | 43.20%          | 35.86%          | 36.02%          | 59.84%          | 46.34%          | 35.38%          | 52.19%          |
| 2018       | -39.24%         | -18.17%         | -42.84%         | -9.50%          | -4.54%          | -34.82%         | -14.69%         | -7.38%          | -25.41%         |
| 2019       | 61.25%          | 71.77%          | 64.03%          | 25.31%          | 36.58%          | 62.92%          | 23.15%          | 20.82%          | 44.93%          |
| 2020       | 127.76%         | 606.06%         | 261.50%         | 207.22%         | 374.52%         | 228.67%         | 159.39%         | 191.53%         | 127.00%         |
| 2021       | 142.64%         | 62.82%          | 60.80%          | 66.70%          | 6.84%           | 12.85%          | 44.13%          | 12.79%          | 10.37%          |
| 2022       | -36.29%         | -40.09%         | -19.46%         | -25.15%         | -24.72%         | 12.10%          | -27.36%         | -31.72%         | 5.97%           |
| 2023       | 222.98%         | 127.87%         | 65.65%          | 117.94%         | 65.27%          | 64.08%          | 56.10%          | 33.70%          | 44.24%          |
| 2024       | -15.61%         | -34.72%         | -11.78%         | 25.68%          | -1.39%          | -4.75%          | 23.86%          | 13.88%          | 19.89%          |
| 2025       | 43.00%          | 96.03%          | 22.44%          | 133.50%         | 159.93%         | 109.77%         | 124.20%         | 117.88%         | 96.07%          |
| 2026 (YTD) | 150.93%         | 71.97%          | 16.67%          | 179.88%         | 100.06%         | 37.68%          | 131.47%         | 64.79%          | 23.93%          |

### Benchmark Comparison Summary vs QQQ

This table compares each strategy combination with QQQ using the same non-overlapping holding-period path.

|   Top N |   Holding Months |   Years | Avg Strategy Yearly Return   | Avg QQQ Yearly Return   | Avg Excess Return   | Beat Rate vs QQQ   | Best Excess   | Worst Excess   |
|--------:|-----------------:|--------:|:-----------------------------|:------------------------|:--------------------|:-------------------|:--------------|:---------------|
|       1 |                1 |      11 | 68.88%                       | 22.45%                  | 46.42%              | 72.73%             | 169.71%       | -43.10%        |
|       1 |                2 |      11 | 99.20%                       | 21.44%                  | 77.76%              | 72.73%             | 562.16%       | -62.21%        |
|       1 |                3 |      11 | 47.38%                       | 20.10%                  | 27.28%              | 81.82%             | 217.59%       | -41.39%        |
|       2 |                1 |      11 | 73.40%                       | 22.45%                  | 50.94%              | 72.73%             | 163.32%       | -15.41%        |
|       2 |                2 |      11 | 74.94%                       | 21.44%                  | 53.50%              | 63.64%             | 330.61%       | -28.88%        |
|       2 |                3 |      11 | 56.01%                       | 20.10%                  | 35.91%              | 72.73%             | 184.76%       | -33.37%        |
|       3 |                1 |      11 | 56.32%                       | 22.45%                  | 33.87%              | 72.73%             | 115.49%       | -17.57%        |
|       3 |                2 |      11 | 46.97%                       | 21.44%                  | 25.54%              | 54.55%             | 147.62%       | -19.90%        |
|       3 |                3 |      11 | 42.37%                       | 20.10%                  | 22.27%              | 63.64%             | 83.09%        | -23.96%        |

### Summary

|   Top N |   Holding Months |   Trades | Avg Return   | Median Return   | Win Rate   | Best Return   | Worst Return   |   Avg Available Universe |
|--------:|-----------------:|---------:|:-------------|:----------------|:-----------|:--------------|:---------------|-------------------------:|
|       1 |                1 |      125 | 4.98%        | 2.84%           | 56.80%     | 81.29%        | -41.01%        |                     92.2 |
|       1 |                2 |      123 | 11.51%       | 7.40%           | 64.23%     | 132.93%       | -40.06%        |                     92.2 |
|       1 |                3 |      122 | 16.54%       | 11.40%          | 63.93%     | 151.03%       | -48.38%        |                     92.1 |
|       2 |                1 |      125 | 4.92%        | 2.65%           | 64.00%     | 58.37%        | -27.84%        |                     92.2 |
|       2 |                2 |      123 | 9.80%        | 5.69%           | 73.17%     | 100.59%       | -33.45%        |                     92.2 |
|       2 |                3 |      122 | 14.33%       | 9.92%           | 72.95%     | 144.33%       | -35.86%        |                     92.1 |
|       3 |                1 |      125 | 3.97%        | 2.05%           | 64.00%     | 54.71%        | -22.64%        |                     92.2 |
|       3 |                2 |      123 | 7.92%        | 4.71%           | 70.73%     | 127.56%       | -29.65%        |                     92.2 |
|       3 |                3 |      122 | 11.52%       | 8.03%           | 75.41%     | 100.05%       | -33.11%        |                     92.1 |

### Latest Top-3 Monthly Selections

This table follows the same compact display style as the previous project: it only shows the latest Top-3 monthly selections, their momentum values, and the realized 1M holding returns.

| Decision Month   | Decision Date   | Top 1   | Top 1 Momentum   | Top 1 Return   | Top 2   | Top 2 Momentum   | Top 2 Return   | Top 3   | Top 3 Momentum   | Top 3 Return   | Avg Momentum   | Portfolio Hold 1M Return   |
|:-----------------|:----------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:---------------|:---------------------------|
| 2025-06          | 2025-06-02      | PLTR    | 12.67%           | -1.03%         | ZS      | 10.61%           | 4.82%          | MELI    | 8.39%            | -3.55%         | 10.56%         | 0.08%                      |
| 2025-07          | 2025-07-01      | PLTR    | 10.19%           | 18.05%         | ZS      | 9.55%            | -8.80%         | MCHP    | 8.24%            | -7.42%         | 9.33%          | 0.61%                      |
| 2025-08          | 2025-08-01      | PLTR    | 13.88%           | 1.83%          | AMD     | 12.43%           | -5.46%         | AVGO    | 9.81%            | 3.33%          | 12.04%         | -0.10%                     |
| 2025-09          | 2025-09-02      | PLTR    | 13.94%           | 17.74%         | APP     | 13.22%           | 46.16%         | AVGO    | 12.44%           | 11.98%         | 13.20%         | 25.29%                     |
| 2025-10          | 2025-10-01      | APP     | 22.68%           | -10.22%        | MU      | 20.58%           | 28.93%         | WBD     | 20.50%           | 15.19%         | 21.25%         | 11.30%                     |
| 2025-11          | 2025-11-03      | MU      | 21.12%           | 2.45%          | WBD     | 19.81%           | 7.09%          | AMD     | 19.76%           | -15.36%        | 20.23%         | -1.94%                     |
| 2025-12          | 2025-12-01      | WBD     | 19.35%           | 19.44%         | MU      | 16.99%           | 31.23%         | APP     | 14.85%           | -0.85%         | 17.06%         | 16.61%                     |
| 2026-01          | 2026-01-02      | MU      | 25.86%           | 38.80%         | WDC     | 21.20%           | 43.97%         | WBD     | 19.71%           | -3.47%         | 22.26%         | 26.43%                     |
| 2026-02          | 2026-02-02      | MU      | 31.03%           | -5.74%         | WDC     | 28.59%           | -0.06%         | STX     | 22.71%           | -12.34%        | 27.44%         | -6.05%                     |
| 2026-03          | 2026-03-02      | MU      | 19.13%           | -10.82%        | WDC     | 16.66%           | 10.29%         | AMAT    | 11.54%           | -4.94%         | 15.78%         | -1.82%                     |
| 2026-04          | 2026-04-01      | WDC     | 14.51%           | 44.94%         | STX     | 11.67%           | 71.80%         | MU      | 11.18%           | 47.40%         | 12.46%         | 54.71%                     |
| 2026-05          | 2026-05-01      | SNDK    | 49.79%           | 48.39%         | INTC    | 25.71%           | 9.75%          | STX     | 25.69%           | 26.73%         | 33.73%         | 28.29%                     |

_Note: The ranking is still recomputed using the Nasdaq-100 universe effective at each decision date. Universe audit fields are kept in `output/momentum_grid_detail.csv`, but are intentionally omitted here to keep the README readable._

## 6-Month Momentum Strategy

### Backtest Yearly Compounded Returns

The table below uses non-overlapping compounding paths starting from January. Hold 1M compounds monthly decisions Jan through Dec, Hold 2M compounds Jan/Mar/May/Jul/Sep/Nov decisions, and Hold 3M compounds Jan/Apr/Jul/Oct decisions. The current year is labelled YTD when it is incomplete.

| Year       | Top 1 Hold 1M   | Top 1 Hold 2M   | Top 1 Hold 3M   | Top 2 Hold 1M   | Top 2 Hold 2M   | Top 2 Hold 3M   | Top 3 Hold 1M   | Top 3 Hold 2M   | Top 3 Hold 3M   |
|:-----------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|
| 2016       | 130.52%         | 149.63%         | 129.23%         | 89.06%          | 61.42%          | 38.55%          | 67.53%          | 58.42%          | 48.80%          |
| 2017       | 20.61%          | 20.08%          | 43.20%          | 23.10%          | 40.19%          | 64.12%          | 32.87%          | 46.14%          | 58.09%          |
| 2018       | -37.74%         | -52.06%         | -57.63%         | -8.32%          | -26.32%         | -27.41%         | -8.96%          | -20.89%         | -13.03%         |
| 2019       | 91.14%          | 108.69%         | 76.13%          | 44.60%          | 49.39%          | 40.96%          | 55.60%          | 52.67%          | 39.99%          |
| 2020       | 130.69%         | 261.50%         | 689.80%         | 259.41%         | 350.75%         | 309.03%         | 227.63%         | 282.42%         | 228.81%         |
| 2021       | 45.93%          | 47.01%          | 60.80%          | 34.03%          | 26.27%          | 36.00%          | 32.37%          | 13.02%          | 31.67%          |
| 2022       | -34.50%         | -47.23%         | 23.76%          | -43.10%         | -37.12%         | -30.49%         | -16.42%         | -14.88%         | -25.89%         |
| 2023       | 109.03%         | 115.46%         | 103.44%         | 91.76%          | 98.73%          | 77.58%          | 63.25%          | 67.97%          | 56.53%          |
| 2024       | 7.57%           | 22.18%          | -11.78%         | -20.50%         | -13.84%         | 47.37%          | -21.34%         | -2.66%          | 28.77%          |
| 2025       | 57.11%          | 96.03%          | 22.44%          | 144.68%         | 171.96%         | 109.77%         | 100.70%         | 117.73%         | 69.15%          |
| 2026 (YTD) | 160.28%         | 89.14%          | 58.70%          | 134.16%         | 77.59%          | 27.56%          | 132.57%         | 60.67%          | 23.93%          |

### Benchmark Comparison Summary vs QQQ

This table compares each strategy combination with QQQ using the same non-overlapping holding-period path.

|   Top N |   Holding Months |   Years | Avg Strategy Yearly Return   | Avg QQQ Yearly Return   | Avg Excess Return   | Beat Rate vs QQQ   | Best Excess   | Worst Excess   |
|--------:|-----------------:|--------:|:-----------------------------|:------------------------|:--------------------|:-------------------|:--------------|:---------------|
|       1 |                1 |      11 | 61.88%                       | 22.45%                  | 39.42%              | 63.64%             | 138.99%       | -36.29%        |
|       1 |                2 |      11 | 73.68%                       | 21.44%                  | 52.24%              | 63.64%             | 217.59%       | -50.61%        |
|       1 |                3 |      11 | 103.46%                      | 20.10%                  | 83.36%              | 81.82%             | 645.89%       | -56.17%        |
|       2 |                1 |      11 | 68.08%                       | 22.45%                  | 45.63%              | 63.64%             | 215.50%       | -47.99%        |
|       2 |                2 |      11 | 72.64%                       | 21.44%                  | 51.20%              | 63.64%             | 306.84%       | -41.33%        |
|       2 |                3 |      11 | 63.00%                       | 20.10%                  | 42.90%              | 90.91%             | 265.13%       | -25.96%        |
|       3 |                1 |      11 | 60.53%                       | 22.45%                  | 38.07%              | 72.73%             | 183.72%       | -48.83%        |
|       3 |                2 |      11 | 60.06%                       | 21.44%                  | 38.62%              | 72.73%             | 238.52%       | -30.15%        |
|       3 |                3 |      11 | 49.71%                       | 20.10%                  | 29.61%              | 81.82%             | 184.91%       | -11.58%        |

### Summary

|   Top N |   Holding Months |   Trades | Avg Return   | Median Return   | Win Rate   | Best Return   | Worst Return   |   Avg Available Universe |
|--------:|-----------------:|---------:|:-------------|:----------------|:-----------|:--------------|:---------------|-------------------------:|
|       1 |                1 |      125 | 4.81%        | 1.83%           | 56.80%     | 81.29%        | -41.01%        |                     92.2 |
|       1 |                2 |      124 | 11.19%       | 7.11%           | 62.90%     | 132.93%       | -40.06%        |                     92.1 |
|       1 |                3 |      123 | 16.59%       | 8.01%           | 61.79%     | 164.48%       | -48.77%        |                     92.1 |
|       2 |                1 |      124 | 4.28%        | 1.91%           | 61.29%     | 46.17%        | -27.84%        |                     92.2 |
|       2 |                2 |      123 | 9.78%        | 5.59%           | 67.48%     | 132.48%       | -33.45%        |                     92.2 |
|       2 |                3 |      122 | 14.34%       | 10.94%          | 70.49%     | 144.33%       | -38.19%        |                     92.1 |
|       3 |                1 |      124 | 4.07%        | 2.24%           | 58.87%     | 54.71%        | -24.20%        |                     92.2 |
|       3 |                2 |      123 | 9.01%        | 7.24%           | 69.11%     | 127.56%       | -30.38%        |                     92.2 |
|       3 |                3 |      122 | 12.17%       | 8.80%           | 73.77%     | 100.05%       | -33.11%        |                     92.1 |

### Latest Top-3 Monthly Selections

This table follows the same compact display style as the previous project: it only shows the latest Top-3 monthly selections, their momentum values, and the realized 1M holding returns.

| Decision Month   | Decision Date   | Top 1   | Top 1 Momentum   | Top 1 Return   | Top 2   | Top 2 Momentum   | Top 2 Return   | Top 3   | Top 3 Momentum   | Top 3 Return   | Avg Momentum   | Portfolio Hold 1M Return   |
|:-----------------|:----------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:---------------|:---------------------------|
| 2025-06          | 2025-06-02      | PLTR    | 12.77%           | -1.03%         | AVGO    | 8.83%            | 6.70%          | ZS      | 6.69%            | 4.82%          | 9.43%          | 3.50%                      |
| 2025-07          | 2025-07-01      | PLTR    | 10.39%           | 18.05%         | ZS      | 9.64%            | -8.80%         | NFLX    | 6.83%            | -10.44%        | 8.95%          | -0.40%                     |
| 2025-08          | 2025-08-01      | PLTR    | 11.50%           | 1.83%          | AMD     | 8.02%            | -5.46%         | NVDA    | 7.28%            | -1.69%         | 8.93%          | -1.78%                     |
| 2025-09          | 2025-09-02      | PLTR    | 11.87%           | 17.74%         | AMD     | 9.45%            | 1.04%          | AVGO    | 8.73%            | 11.98%         | 10.02%         | 10.25%                     |
| 2025-10          | 2025-10-01      | APP     | 18.71%           | -10.22%        | MU      | 15.10%           | 28.93%         | PLTR    | 14.57%           | 12.02%         | 16.13%         | 10.24%                     |
| 2025-11          | 2025-11-03      | MU      | 21.98%           | 2.45%          | WBD     | 19.61%           | 7.09%          | AMD     | 19.56%           | -15.36%        | 20.38%         | -1.94%                     |
| 2025-12          | 2025-12-01      | MU      | 18.01%           | 31.23%         | WBD     | 17.69%           | 19.44%         | INTC    | 14.21%           | -1.57%         | 16.64%         | 16.36%                     |
| 2026-01          | 2026-01-02      | WDC     | 20.98%           | 43.97%         | WBD     | 19.36%           | -3.47%         | MU      | 19.36%           | 38.80%         | 19.90%         | 26.43%                     |
| 2026-02          | 2026-02-02      | MU      | 28.02%           | -5.74%         | WDC     | 24.99%           | -0.06%         | STX     | 20.61%           | -12.34%        | 24.54%         | -6.05%                     |
| 2026-03          | 2026-03-02      | MU      | 24.90%           | -10.82%        | WDC     | 23.82%           | 10.29%         | WBD     | 18.06%           | -3.54%         | 22.26%         | -1.36%                     |
| 2026-04          | 2026-04-01      | WDC     | 15.59%           | 44.94%         | MU      | 14.14%           | 47.40%         | STX     | 10.29%           | 71.80%         | 13.34%         | 54.71%                     |
| 2026-05          | 2026-05-01      | SNDK    | 41.75%           | 48.39%         | STX     | 21.69%           | 26.73%         | INTC    | 21.64%           | 9.75%          | 28.36%         | 28.29%                     |

_Note: The ranking is still recomputed using the Nasdaq-100 universe effective at each decision date. Universe audit fields are kept in `output/momentum_grid_detail.csv`, but are intentionally omitted here to keep the README readable._

## 7-Month Momentum Strategy

### Backtest Yearly Compounded Returns

The table below uses non-overlapping compounding paths starting from January. Hold 1M compounds monthly decisions Jan through Dec, Hold 2M compounds Jan/Mar/May/Jul/Sep/Nov decisions, and Hold 3M compounds Jan/Apr/Jul/Oct decisions. The current year is labelled YTD when it is incomplete.

| Year       | Top 1 Hold 1M   | Top 1 Hold 2M   | Top 1 Hold 3M   | Top 2 Hold 1M   | Top 2 Hold 2M   | Top 2 Hold 3M   | Top 3 Hold 1M   | Top 3 Hold 2M   | Top 3 Hold 3M   |
|:-----------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|:----------------|
| 2016       | 150.27%         | 123.47%         | 166.71%         | 57.74%          | 38.03%          | 67.26%          | 66.02%          | 52.80%          | 49.62%          |
| 2017       | 32.53%          | -5.87%          | 19.88%          | 35.25%          | 30.72%          | 38.66%          | 47.24%          | 57.26%          | 53.28%          |
| 2018       | 7.70%           | -25.29%         | -16.14%         | -3.63%          | -20.95%         | -31.00%         | 5.07%           | -7.24%          | -13.34%         |
| 2019       | 123.14%         | 104.66%         | 76.13%          | 83.79%          | 54.73%          | 48.51%          | 46.59%          | 31.86%          | 41.66%          |
| 2020       | 895.58%         | 895.58%         | 288.16%         | 208.79%         | 319.14%         | 247.96%         | 201.71%         | 234.30%         | 160.25%         |
| 2021       | 86.15%          | 47.01%          | 60.80%          | 24.94%          | 10.10%          | 8.81%           | -4.34%          | 1.07%           | 8.03%           |
| 2022       | -46.55%         | -55.94%         | -59.27%         | -30.12%         | -28.76%         | -25.97%         | -35.15%         | -25.05%         | -34.63%         |
| 2023       | 55.56%          | 35.23%          | 52.54%          | 56.05%          | 60.83%          | 34.43%          | 42.04%          | 43.20%          | 40.62%          |
| 2024       | -29.12%         | 11.42%          | -21.31%         | 0.49%           | 32.17%          | 29.58%          | 15.52%          | 67.61%          | 20.10%          |
| 2025       | 57.11%          | 96.03%          | 22.44%          | 53.63%          | 129.32%         | 40.69%          | 107.47%         | 116.08%         | 87.35%          |
| 2026 (YTD) | 175.98%         | 89.14%          | 58.70%          | 158.31%         | 100.06%         | 37.68%          | 144.44%         | 101.15%         | 23.93%          |

### Benchmark Comparison Summary vs QQQ

This table compares each strategy combination with QQQ using the same non-overlapping holding-period path.

|   Top N |   Holding Months |   Years | Avg Strategy Yearly Return   | Avg QQQ Yearly Return   | Avg Excess Return   | Beat Rate vs QQQ   | Best Excess   | Worst Excess   |
|--------:|-----------------:|--------:|:-----------------------------|:------------------------|:--------------------|:-------------------|:--------------|:---------------|
|       1 |                1 |      11 | 137.12%                      | 22.45%                  | 114.67%             | 72.73%             | 851.68%       | -56.61%        |
|       1 |                2 |      11 | 119.59%                      | 21.44%                  | 98.15%              | 54.55%             | 851.68%       | -39.66%        |
|       1 |                3 |      11 | 58.97%                       | 20.10%                  | 38.86%              | 54.55%             | 244.25%       | -48.80%        |
|       2 |                1 |      11 | 58.66%                       | 22.45%                  | 36.20%              | 72.73%             | 164.88%       | -27.00%        |
|       2 |                2 |      11 | 65.95%                       | 21.44%                  | 44.51%              | 72.73%             | 275.24%       | -20.39%        |
|       2 |                3 |      11 | 45.15%                       | 20.10%                  | 25.05%              | 72.73%             | 204.05%       | -29.55%        |
|       3 |                1 |      11 | 57.87%                       | 22.45%                  | 35.42%              | 63.64%             | 157.80%       | -34.82%        |
|       3 |                2 |      11 | 61.19%                       | 21.44%                  | 39.75%              | 63.64%             | 190.40%       | -29.42%        |
|       3 |                3 |      11 | 39.72%                       | 20.10%                  | 19.61%              | 54.55%             | 116.34%       | -22.46%        |

### Summary

|   Top N |   Holding Months |   Trades | Avg Return   | Median Return   | Win Rate   | Best Return   | Worst Return   |   Avg Available Universe |
|--------:|-----------------:|---------:|:-------------|:----------------|:-----------|:--------------|:---------------|-------------------------:|
|       1 |                1 |      125 | 6.37%        | 3.38%           | 60.80%     | 81.29%        | -35.24%        |                     92.2 |
|       1 |                2 |      123 | 13.06%       | 9.25%           | 63.41%     | 132.93%       | -40.06%        |                     92.2 |
|       1 |                3 |      122 | 16.70%       | 8.02%           | 61.48%     | 164.48%       | -61.25%        |                     92.1 |
|       2 |                1 |      125 | 4.11%        | 2.72%           | 62.40%     | 46.17%        | -27.84%        |                     92.2 |
|       2 |                2 |      123 | 9.07%        | 5.15%           | 65.85%     | 132.48%       | -33.45%        |                     92.2 |
|       2 |                3 |      122 | 12.48%       | 8.86%           | 69.67%     | 144.33%       | -38.19%        |                     92.1 |
|       3 |                1 |      125 | 3.92%        | 2.55%           | 63.20%     | 54.71%        | -22.46%        |                     92.2 |
|       3 |                2 |      123 | 8.35%        | 6.11%           | 65.85%     | 127.56%       | -29.65%        |                     92.2 |
|       3 |                3 |      122 | 11.10%       | 8.42%           | 76.23%     | 132.18%       | -33.61%        |                     92.1 |

### Latest Top-3 Monthly Selections

This table follows the same compact display style as the previous project: it only shows the latest Top-3 monthly selections, their momentum values, and the realized 1M holding returns.

| Decision Month   | Decision Date   | Top 1   | Top 1 Momentum   | Top 1 Return   | Top 2   | Top 2 Momentum   | Top 2 Return   | Top 3   | Top 3 Momentum   | Top 3 Return   | Avg Momentum   | Portfolio Hold 1M Return   |
|:-----------------|:----------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:--------|:-----------------|:---------------|:---------------|:---------------------------|
| 2025-06          | 2025-06-02      | PLTR    | 19.28%           | -1.03%         | APP     | 19.19%           | -16.23%        | MSTR    | 10.95%           | 0.28%          | 16.47%         | -5.66%                     |
| 2025-07          | 2025-07-01      | PLTR    | 10.80%           | 18.05%         | AVGO    | 8.52%            | 9.03%          | ZS      | 6.43%            | -8.80%         | 8.58%          | 6.09%                      |
| 2025-08          | 2025-08-01      | PLTR    | 11.48%           | 1.83%          | ZS      | 7.01%            | -2.03%         | CEG     | 6.71%            | -9.75%         | 8.40%          | -3.32%                     |
| 2025-09          | 2025-09-02      | PLTR    | 10.12%           | 17.74%         | AMD     | 6.09%            | 1.04%          | APP     | 6.03%            | 46.16%         | 7.41%          | 21.64%                     |
| 2025-10          | 2025-10-01      | APP     | 13.72%           | -10.22%        | PLTR    | 12.71%           | 12.02%         | MU      | 12.67%           | 28.93%         | 13.03%         | 10.24%                     |
| 2025-11          | 2025-11-03      | MU      | 17.07%           | 2.45%          | AMD     | 15.92%           | -15.36%        | APP     | 14.58%           | -1.35%         | 15.86%         | -4.75%                     |
| 2025-12          | 2025-12-01      | MU      | 19.19%           | 31.23%         | WBD     | 17.82%           | 19.44%         | AMD     | 14.57%           | 1.69%          | 17.19%         | 17.45%                     |
| 2026-01          | 2026-01-02      | WDC     | 21.21%           | 43.97%         | MU      | 19.90%           | 38.80%         | WBD     | 17.94%           | -3.47%         | 19.68%         | 26.43%                     |
| 2026-02          | 2026-02-02      | WDC     | 24.27%           | -0.06%         | MU      | 22.14%           | -5.74%         | STX     | 18.63%           | -12.34%        | 21.68%         | -6.05%                     |
| 2026-03          | 2026-03-02      | MU      | 23.20%           | -10.82%        | WDC     | 21.41%           | 10.29%         | STX     | 15.90%           | 11.68%         | 20.17%         | 3.72%                      |
| 2026-04          | 2026-04-01      | WDC     | 21.88%           | 44.94%         | MU      | 19.80%           | 47.40%         | STX     | 16.12%           | 71.80%         | 19.27%         | 54.71%                     |
| 2026-05          | 2026-05-01      | SNDK    | 45.91%           | 48.39%         | INTC    | 19.97%           | 9.75%          | WDC     | 19.79%           | 26.58%         | 28.56%         | 28.24%                     |

_Note: The ranking is still recomputed using the Nasdaq-100 universe effective at each decision date. Universe audit fields are kept in `output/momentum_grid_detail.csv`, but are intentionally omitted here to keep the README readable._


## How to Run

```bash
pip install -r requirements.txt
python run_all.py
```

Generated outputs are saved in `output/`.

Important output files:

- `data/nasdaq100_current_tickers.csv`: current Nasdaq-100 list downloaded from Wikipedia.
- `data/nasdaq100_component_changes.csv`: component changes parsed from Wikipedia.
- `data/nasdaq100_all_historical_tickers.csv`: all current, added, and removed tickers used for price downloads.
- `output/momentum_grid_detail.csv`: full monthly selections, effective universe date, selected stocks, momentum, and holding returns.
- `output/yearly_compounded_returns.csv`: annual compounded return table for all 3/4/5/6/7-month momentum windows.
- `output/momentum_grid_summary.csv`: strategy summary statistics.
- `output/benchmark_comparison_summary.csv`: QQQ comparison summary.
