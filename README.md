# US options positioning history — max pain, gamma exposure (GEX), walls, IV and put/call, daily since 2008

Daily, end-of-day **options positioning data** for SPY, QQQ and 20 large US stocks: one CSV row per trading session with
max pain (front, monthly, all expiries), dealer gamma exposure (GEX) by horizon, gamma flip, call and put walls, implied
volatility at constant tenors, IV rank, skew, put/call ratios, open interest and volume — **118 columns**, computed
from end-of-day option chains. The largest names go back to **January 2008**.

This is a sample. The same series for **1,478 US stocks and ETFs**, plus each ticker's strike, expiry and horizon
tables, is on **[spyforecast.com/historical-options-data](https://spyforecast.com/historical-options-data/)** (no account). Each ticker also has a page with
today's levels, e.g. [SPY](https://spyforecast.com/etf/spy.html) · [NVDA](https://spyforecast.com/stock/nvda.html) · [TSLA](https://spyforecast.com/stock/tsla.html).

Last session in this copy: **2026-11-13**. Refreshed every week.

## Files

| File | What |
|---|---|
| `data/<TICKER>.csv` | the daily option series, one row per session, oldest first (`date` = YYYY-MM-DD) |
| `index.csv` | ticker, name, first and last session, number of sessions |
| `columns.csv` | every column: group, unit, label, what it is |
| `quickstart.ipynb` · `quickstart.py` | load, put the levels on the price scale, gamma regime vs next-day moves (with an IV control) |

| Ticker | Name | From | Sessions |
|---|---|---|---:|
| SPY | S&P 500 | 2008-01-02 | 4,745 |
| QQQ | Nasdaq 100 | 2011-03-23 | 3,934 |
| AAPL | Apple | 2008-01-02 | 4,642 |
| MSFT | Microsoft | 2008-01-02 | 4,746 |
| NVDA | NVIDIA | 2008-01-02 | 4,746 |
| AMZN | Amazon.com | 2008-01-02 | 4,645 |
| GOOGL | Alphabet | 2013-01-02 | 3,298 |
| META | Meta Platforms | 2021-07-08 | 1,256 |
| TSLA | Tesla | 2010-07-08 | 4,113 |
| AMD | Advanced Micro Devices | 2008-01-02 | 4,745 |
| AVGO | Broadcom | 2009-08-24 | 4,332 |
| NFLX | Netflix | 2008-01-02 | 4,745 |
| PLTR | Palantir Technologies | 2020-10-06 | 1,535 |
| JPM | JPMorgan Chase & | 2008-01-02 | 4,601 |
| BAC | Bank of America | 2008-01-02 | 4,744 |
| XOM | ExxonMobil Holdings | 2008-01-02 | 4,746 |
| INTC | Intel | 2013-01-02 | 3,439 |
| COIN | Coinbase Global | 2021-04-20 | 1,391 |
| MSTR | Strategy | 2013-01-02 | 3,440 |
| BA | The Boeing | 2008-01-02 | 4,744 |
| DIS | The Walt Disney | 2008-01-02 | 4,746 |
| WMT | Walmart | 2008-01-02 | 4,652 |

## Quick start

```python
import pandas as pd

df = pd.read_csv("data/SPY.csv", parse_dates=["date"]).set_index("date")
for c in ["max_pain_front", "max_pain_monthly", "call_wall_near", "put_wall_near", "gamma_flip"]:
    df[c] = df[c] * df["split_factor"]          # strike levels on the same scale as the close

print(df[["close", "max_pain_monthly", "gex", "pc_oi_ratio", "iv30"]].tail())
```

## Read this before a backtest

- **End-of-day only.** Each row is the chain captured after that session's close. Nothing in a row uses a later session; rolling figures (IV rank, realised volatility, relative volume) look back only.
- **A blank cell means "no value that session"**, never zero. When the chain of a session was not a usable picture of the book, `chain_flag` ≠ 0 and the option cells are blank.
- **Open interest is the previous close**: an end-of-day chain carries the open interest published that morning, so `*_oi_chg` mostly describes the previous session's trading.
- **Strike levels are not split-adjusted** (walls, max pain, gamma flip, spot); `close` is. Multiply a level by `split_factor`.
- **Same-day expiries are left out** of open interest, greeks, walls and max pain (their share is `oi_0dte_share`); volume columns count every contract.
- **IV is a decimal** (0.25 = 25 %); percent columns are 0–100.
- **One change of method:** from the session of 2026-11-13 implied volatility and greeks come from a recomputed source; near-the-money IV differs by ~0.7 vol points on average, so IV-based columns can step at that date.
- GEX assumes dealers are long calls and short puts — an estimate, as everywhere GEX is published.
- Full price bars (open, high, low, volume) are not included; `close` is.

## Column groups

- **Price**: `date`, `close`, `spot`, `split_factor`, `bar_from_chain`
- **Implied volatility**: `iv30`, `iv10`, `iv20`, `iv60`, `iv90`, `iv180`, `iv_rank_1y`, `iv_pctl_1y`, `hv20`, `iv_hv_spread`, `term_slope`, `term_slope_short`, `skew25`, `front_atm_iv`, `front_skew25`, `exp_move_30d`, `exp_move_30d_pct`, `exp_move_front`, `front_dte`
- **Open interest & volume**: `call_oi`, `put_oi`, `total_oi`, `call_oi_chg`, `put_oi_chg`, `total_oi_chg`, `call_vol`, `put_vol`, `total_vol`, `rel_vol_20`, `pc_oi_ratio`, `pc_vol_ratio`, `put_share_oi`, `vol_oi_ratio`, `call_premium`, `put_premium`, `net_premium`, `delta_flow`, `near_oi_share`, `front_oi_share`, `oi_0dte_share`
- **Dealer positioning (greeks)**: `gex`, `gex_0_14d`, `gex_per_oi`, `gamma_regime`, `spot_vs_flip_pct`, `dex`, `vanna`, `charm`, `vega`, `gex_15_45d`, `gex_46_180d`, `gex_181d_plus`, `vanna_0_14d`, `charm_0_14d`, `spot_vs_delta_flip_pct`, `delta_tilt`, `delta_net_near`, `delta_share_near`, `vex`, `chex`, `vex_0_14d`, `chex_0_14d`, `vex_15_45d`, `chex_15_45d`, `vex_46_180d`, `chex_46_180d`
- **Levels (strikes)**: `gamma_flip`, `call_wall`, `call_wall_oi`, `call_wall_2`, `put_wall`, `put_wall_oi`, `put_wall_2`, `gamma_wall_up`, `gamma_wall_down`, `max_pain_front`, `max_pain_monthly`, `call_wall_pct`, `put_wall_pct`, `max_pain_front_pct`, `delta_flip`, `call_wall_3`, `put_wall_3`, `call_oi_peak`, `put_oi_peak`, `max_pain_all`, `call_wall_0_14d`, `put_wall_0_14d`, `max_pain_0_14d`, `call_wall_15_45d`, `put_wall_15_45d`, `max_pain_15_45d`, `call_wall_46_180d`, `put_wall_46_180d`, `max_pain_46_180d`, `call_wall_near`, `call_wall_near_oi`, `call_wall_near_pct`, `call_wall_near_2`, `put_wall_near`, `put_wall_near_oi`, `put_wall_near_pct`, `put_wall_near_2`
- **Chain quality**: `chain_grade`, `chain_score`, `chain_flag`, `expiries`, `strikes`
- **Call side vs put side**: `adj_atm_pct`, `adj_net_dollar`, `adj_net_rungs`, `delta_price25`, `delta_price25_skew`

Every column is explained in `columns.csv`.

## Licence and source

Computed by [SpyForecast](https://spyforecast.com) from end-of-day option chains; no raw quotes or chains are included.
Licensed **CC BY-NC-SA 4.0** — use, share and adapt for non-commercial purposes with credit
("SpyForecast, spyforecast.com"). For research and education; not investment advice.
