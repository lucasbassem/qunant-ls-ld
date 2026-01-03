# Strategy & Research Spec (Contract)

## Objective
Build a research-grade, leakage-safe long/short US equity strategy that predicts next-day **open→close** returns using features available by the **close of day t**.

## Universe
- US equities
- Select top **300** tickers by trailing **20-trading-day median dollar volume** (Close × Volume)
- Reconstitute **monthly** on the first trading day of each month
- Exclude tickers missing required data for the trade day

## Data
Daily OHLCV:
- Date, Open, High, Low, Close, Volume
- Use adjusted pricing consistently (document the adjustment choice)

## Signal Timing
- Features computed using data available **up to close(t)**
- No use of open/close/high/low/volume from t+1 or later in features

## Label (Prediction Target)
For each ticker i on day t:

y(i,t) = Close(i,t+1) / Open(i,t+1) - 1

## Trading Rule
- Compute predictions after **close(t)**
- Enter positions at **open(t+1)**
- Exit positions at **close(t+1)**
- Holding period: **1 trading day**

## Portfolio Construction (Dollar-Neutral)
Daily at close(t):
- Rank tickers by predicted y(i,t)
- Long: top **10%**
- Short: bottom **10%**
- Equal-weight within each leg
- Scale weights so:
  - sum(long weights) = +0.5
  - sum(short weights) = -0.5
- Net exposure ≈ 0 (dollar-neutral)

## Filters
- Drop any ticker without Open(t+1) and Close(t+1)
- Optional: exclude Close(t) < $5 (if used, keep consistent and document)

## Transaction Costs
- Turnover(t) = sum over tickers of |w(t) - w(t-1)|
- Cost(t) = Turnover(t) × (cost_bps / 10,000)
- Report results for cost_bps ∈ {0, 5, 10, 20}

## Validation
- Walk-forward evaluation (expanding training window, fixed test window)
- No random shuffling
- Report fold-by-fold performance and aggregate metrics

## Metrics to Report
- Annualized Sharpe (daily)
- Max drawdown
- Annualized return (optional) and volatility
- Average daily turnover
- Cost sensitivity (0/5/10/20 bps)
