from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Need 2015 data so 2016-01 can have valid 3-7 month momentum signals.
START_DATE = "2015-01-01"
BACKTEST_START = "2016-01-01"

# Strategy grid.
MOMENTUM_WINDOWS = [3, 4, 5, 6, 7]
TOP_NS = [1, 2, 3]
HOLDING_MONTHS = [1, 2, 3]

BENCHMARK_TICKER = "QQQ"
WIKI_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"

CURRENT_TICKERS_FILE = DATA_DIR / "nasdaq100_current_tickers.csv"
COMPONENT_CHANGES_FILE = DATA_DIR / "nasdaq100_component_changes.csv"
ALL_HISTORICAL_TICKERS_FILE = DATA_DIR / "nasdaq100_all_historical_tickers.csv"
PRICE_FILE = DATA_DIR / "nasdaq100_prices.csv"
BENCHMARK_PRICE_FILE = DATA_DIR / "qqq_prices.csv"

DETAIL_FILE = OUTPUT_DIR / "momentum_grid_detail.csv"
SUMMARY_FILE = OUTPUT_DIR / "momentum_grid_summary.csv"
YEARLY_RETURNS_FILE = OUTPUT_DIR / "yearly_compounded_returns.csv"
BENCHMARK_DETAIL_FILE = OUTPUT_DIR / "qqq_benchmark_detail.csv"
BENCHMARK_YEARLY_FILE = OUTPUT_DIR / "qqq_benchmark_yearly_compounded_returns.csv"
BENCHMARK_COMPARISON_FILE = OUTPUT_DIR / "benchmark_comparison_summary.csv"
README_FILE = PROJECT_ROOT / "README.md"
