from datetime import datetime, timedelta

import pandas as pd
from loguru import logger

from provider import yahoo, alpha_vantage


def explore_ret(df: pd.DataFrame):
    print(df.head())
    print(df.tail())
    print(df.nlargest(10, 'Ret'))
    print(df.nsmallest(10, 'Ret'))


def handle_abnormal_data(df: pd.DataFrame, symbol, allow_0_open=False, allow_0_close=False, allow_same_ohlc=False):
    if not allow_0_open:
        zero_open = df['Open'] <= 0
        logger.info(f'Delete {zero_open.sum()} rows for 0 open price, {symbol}')
        df = df[~zero_open]

    if not allow_0_close:
        zero_close = df['Close'] <= 0
        logger.info(f'Delete {zero_close.sum()} rows for 0 close price, {symbol}')
        df = df[~zero_close]

    if not allow_same_ohlc:
        same_ohlc = df[['Open', 'High', 'Low', 'Close']].apply(lambda row: row.nunique() == 1, axis=1)
        logger.info(f'Delete {same_ohlc.sum()} rows for same OHLC, {symbol}')
        df = df[~same_ohlc]
        return df


def generate_daily_ret_df(symbol, provider='yahoo', method='close', years=None):
    if provider == 'yahoo':
        df: pd.DataFrame = yahoo.daily(symbol)
    elif provider == 'alpha':
        time_series_data = alpha_vantage.time_series_daily(symbol, 'full')
        df = pd.DataFrame.from_dict(time_series_data, orient="index")
        df = df.iloc[:, :-2]
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. adjusted close": "Adj Close",
            "6. volume": "Volume",
        })
        df = df.astype({"Open": float, "High": float, "Low": float, "Close": float, "Adj Close": float, "Volume": int})
        df.index = pd.to_datetime(df.index)
    else:
        raise NotImplementedError(f'Unknown provider {provider}')
    df.sort_index(ascending=True, inplace=True)
    if method == 'close':
        df = df.loc[:, ('Adj Close',)]
        df['Last'] = df['Adj Close'].shift(1)
        df['Ret'] = df['Adj Close'].pct_change() * 100
    elif method == 'openclose':
        df = handle_abnormal_data(df, symbol)
        df = df.loc[:, ('Open', 'Close')]
        df['Ret'] = (df['Close'] / df['Open'] - 1) * 100
    if years:
        df = df[df.index > datetime.today() - timedelta(days=365 * years)]
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    df = df[df['Ret'].notna()]
    return df
