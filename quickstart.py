"""Quick start: load one ticker of the dataset and put its strike levels on the price scale.
More tickers: https://spyforecast.com/historical-options-data/"""
import sys
import pandas as pd

ticker = sys.argv[1] if len(sys.argv) > 1 else "SPY"
df = pd.read_csv(f"data/{ticker}.csv", parse_dates=["date"]).set_index("date")
for c in ["max_pain_front", "max_pain_monthly", "call_wall_near", "put_wall_near", "gamma_flip"]:
    df[c] = df[c] * df["split_factor"]          # strike levels are raw strikes; the close is split-adjusted

print(df[["close", "max_pain_front", "max_pain_monthly", "call_wall_near", "put_wall_near", "gex", "pc_oi_ratio", "iv30"]].tail(10))
