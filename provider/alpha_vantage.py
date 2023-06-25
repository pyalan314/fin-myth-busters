import os
from datetime import timedelta

import requests
from cachier import cachier
from dotenv import load_dotenv
from icecream import ic
from loguru import logger

load_dotenv()


@cachier(stale_after=timedelta(days=1))
def query_data(func_name, **kwargs):
    api_key = os.environ.get('ALPHAV_API')
    if not api_key:
        raise ValueError('ALPHAV_API is not found in .env')
    url = f'https://www.alphavantage.co/query?function={func_name}&apikey={api_key}'
    if kwargs:
        params = '&'.join(f'{k}={v}' for k, v in kwargs.items())
        url = '&'.join((url, params))
    logger.debug(url)
    r = requests.get(url)
    data = r.json()
    return data


def time_series_daily(symbol, output_size='compact'):
    data = query_data('TIME_SERIES_DAILY_ADJUSTED', symbol=symbol, outputsize=output_size)
    try:
        return data['Time Series (Daily)']
    except KeyError as e:
        logger.error(data)
        raise e


if __name__ == '__main__':
    example = time_series_daily('SPY', 'full')
    ic(min(example.keys()))
