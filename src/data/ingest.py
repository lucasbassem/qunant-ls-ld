from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List

import pandas as pd

# We use yfinance only for ingestion convenience.
# If you prefer another source later, keep the output schema identical.
import yfinance as yf


RAW_PATH = Path("data/raw/daily_bars.parquet")


def _download_one(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        progress=False,
        group_by="column",
    )
    if df.empty:
        return df

    df = df.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )[["open", "high", "low", "close", "volume"]]

    df.index = pd.to_datetime(df.index).tz_localize(None)
    df = df.reset_index().rename(columns={"Date": "date"})
    df["ticker"] = ticker

    # Ensure dtypes
    df["volume"] = df["volume"].astype("int64", errors="ignore")
    return df[["date", "ticker", "open", "high", "low", "close", "volume"]]


def download_universe(tickers: Iterable[str], start: str, end: str) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    for t in tickers:
        one = _download_one(t, start, end)
        if not one.empty:
            frames.append(one)
    if not frames:
        return pd.DataFrame(columns=["date", "ticker", "open", "high", "low", "close", "volume"])
    out = pd.concat(frames, ignore_index=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", required=True, help="Comma-separated tickers, e.g. AAPL,MSFT,NVDA")
    ap.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="End date YYYY-MM-DD (exclusive)")
    args = ap.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    df = download_universe(tickers, args.start, args.end)

    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(RAW_PATH, index=False)

    print(f"Wrote {len(df):,} rows to {RAW_PATH}")


if __name__ == "__main__":
    main()
