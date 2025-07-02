import pandas as pd
import numpy as np

#TODO:
#DODAC PRZEKONWERTOWANA DATE Z UNIX DLA ULATWIONEJ CZYTELNOSCI
#
#
#

class RenkoCalculator:

	def __init__(self, historic_tickers : pd.DataFrame, percentage : float):
		self.historic_tickers = historic_tickers
		self.percentage = percentage
		self.renko_chart = []


	def renko(self):
		np_price = self.historic_tickers['price'].to_numpy()
		np_volume = self.historic_tickers['quote_qty'].to_numpy()
		np_time = self.historic_tickers['time'].to_numpy()
		summed_volume = 0

		if not self.renko_chart:
			self.renko_chart.append({'time': np_time[0], 'open': np_price[0], 'high': np_price[0], 'low': np_price[0], 'close': np_price[0], 'volume': np_volume[0], 'direction': 'none'})

		up_cont = self.percentage + 1
		up_reversal = (1 - (2 * self.percentage))
		down_cont = 1 - self.percentage
		down_reversal = 2 * self.percentage + 1

		for index, current_price in enumerate(np_price):
			last_brick = self.renko_chart[-1]
			last_close = last_brick['close']
			last_open = last_brick['open']
			last_direction = last_brick['direction']
			summed_volume += np_volume[index]

			if last_direction == 'up':
				req_for_up_continuation = last_close * up_cont
				req_for_up_reversal = last_close * up_reversal

				if current_price >= req_for_up_continuation:
					self.renko_chart.append({'time': np_time[index], 'open': last_close, 'high': current_price, 'low': last_open, 'close': current_price, 'volume': summed_volume, 'direction': 'up'})
					summed_volume = 0

				elif current_price <= req_for_up_reversal:
					self.renko_chart.append({'time': np_time[index], 'open': last_open, 'high': last_close, 'low': current_price, 'close': current_price, 'volume': summed_volume, 'direction': 'down'})
					summed_volume = 0

			elif last_direction == 'down':
				req_for_down_continuation = last_close * down_cont
				req_for_down_reversal = last_close * down_reversal

				if current_price <= req_for_down_continuation:
					self.renko_chart.append({'time': np_time[index], 'open': last_close, 'high': last_close, 'low': current_price, 'close': current_price, 'volume': summed_volume, 'direction': 'down'})
					summed_volume = 0

				elif current_price >= req_for_down_reversal:
					self.renko_chart.append({'time': np_time[index], 'open': last_open, 'high': current_price, 'low': last_open, 'close': current_price, 'volume': summed_volume, 'direction': 'up'})
					summed_volume = 0

			elif last_direction == 'none':
				wzrost = last_close * up_cont
				spadek = last_close * down_cont

				if current_price >= wzrost:
					self.renko_chart.append({'time': np_time[index], 'open': last_close, 'high': current_price, 'low': last_open, 'close': current_price, 'volume': summed_volume, 'direction': 'up'})
					summed_volume = 0

				elif current_price <= spadek:
					self.renko_chart.append({'time': np_time[index], 'open': last_close, 'high': last_close, 'low': current_price, 'close': current_price, 'volume': summed_volume, 'direction': 'down'})
					summed_volume = 0

		return self.renko_chart