import pandas as pd
import numpy as np
from src.utils import get_root

root = get_root()
historic_tickers1 = pd.read_csv(f'{root}/Data/Ticker/Historic/Futures/SUI_USDT/SUIUSDT-trades-2023-05.csv', usecols = ['price', 'time', 'quote_qty'])
percentage1 = 0.005

def renko(historic_tickers: pd.DataFrame, percentage: float):
	"""Oblicza cegiełki Renko na podstawie historycznych danych cenowych.
	:param historic_tickers: DataFrame zawierający co najmniej kolumnę 'price'.
	:param percentage: Procentowy rozmiar cegiełki wyrażony jako ułamek, np. 0.005 dla 0.5%.
	:return: pd.DataFrame z cegiełkami
	"""

	np_price = historic_tickers['price'].to_numpy()
	np_volume = historic_tickers['quote_qty'].to_numpy()
	np_time = historic_tickers['time'].to_numpy()
	renko_chart = []
	summed_volume = 0

	if not renko_chart:
		renko_chart.append({'time': np_time[0], 'open': np_price[0], 'high': np_price[0], 'low': np_price[0], 'close': np_price[0], 'volume': np_volume[0], 'direction': 'none'})

	up_cont = percentage + 1
	up_reversal = (1 - (2 * percentage))
	down_cont = 1 - percentage
	down_reversal = 2 * percentage + 1

	for index, current_price in enumerate(np_price):
		last_brick = renko_chart[-1]
		last_close = last_brick['close']
		last_open = last_brick['open']
		last_direction = last_brick['direction']
		summed_volume += np_volume[index]

		if last_direction == 'up':
			req_for_up_continuation = last_close * up_cont
			req_for_up_reversal = last_close * up_reversal

			if current_price >= req_for_up_continuation:
				renko_chart.append({'time': np_time[index], 'open': last_close, 'high': current_price, 'low': last_open, 'close': current_price, 'volume': summed_volume, 'direction': 'up'})
				summed_volume = 0

			elif current_price <= req_for_up_reversal:
				renko_chart.append({'time': np_time[index], 'open': last_open, 'high': last_close, 'low': current_price, 'close': current_price, 'volume': summed_volume, 'direction': 'down'})
				summed_volume = 0

		elif last_direction == 'down':
			req_for_down_continuation = last_close * down_cont
			req_for_down_reversal = last_close * down_reversal

			if current_price <= req_for_down_continuation:
				renko_chart.append({'time': np_time[index], 'open': last_close, 'high': last_close, 'low': current_price, 'close': current_price, 'volume': summed_volume, 'direction': 'down'})
				summed_volume = 0

			elif current_price >= req_for_down_reversal:
				renko_chart.append({'time': np_time[index], 'open': last_open, 'high': current_price, 'low': last_open, 'close': current_price, 'volume': summed_volume, 'direction': 'up'})
				summed_volume = 0

		elif last_direction == 'none':
			wzrost = last_close * up_cont
			spadek = last_close * down_cont

			if current_price >= wzrost:
				renko_chart.append({'time': np_time[index], 'open': last_close, 'high': current_price, 'low': last_open, 'close': current_price, 'volume': summed_volume, 'direction': 'up'})
				summed_volume = 0

			elif current_price <= spadek:
				renko_chart.append({'time': np_time[index], 'open': last_close, 'high': last_close, 'low': current_price, 'close': current_price, 'volume': summed_volume, 'direction': 'down'})
				summed_volume = 0

	renko_df = pd.DataFrame(renko_chart)
	return renko_df

renko(historic_tickers1, percentage1)