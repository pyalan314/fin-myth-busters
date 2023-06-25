from datetime import timedelta

import pandas as pd
import yfinance as yf
from cachier import cachier


@cachier(stale_after=timedelta(days=1))
def daily(symbol, start=None, end=None, period='max'):
    df: pd.DataFrame = yf.download(symbol, start=start, end=end, period=period, progress=False)
    return df
