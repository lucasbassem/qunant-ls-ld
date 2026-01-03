# Data Schema (Contract)

## Raw daily bars (per ticker)
Index keys:
- date (YYYY-MM-DD)
- ticker (string)

Columns (float unless noted):
- open
- high
- low
- close
- volume (int64)

Derived columns (optional, but if present must be documented):
- dollar_volume = close * volume

## Storage
- Persist as Parquet at: data/raw/daily_bars.parquet
- Partitioning: optional (by year), but start with a single file for simplicity
- Dates must be timezone-naive and represent the US trading day

## Quality rules
- No duplicate (date, ticker)
- Monotonic dates within each ticker
- No negative prices/volume
- Missing values are allowed only if explicitly filtered before labeling/trading
