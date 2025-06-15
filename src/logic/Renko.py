import pandas as pd
import numpy as np
from src.utils import get_root

root = get_root()
historic_tickers1 = pd.read_csv(f'{root}/Data/Ticker/Historic/Futures/SUI_USDT/SUIUSDT-trades-2024-12.csv', usecols = ['price'])
percentage1 = 0.005

def renko(historic_tickers: pd.DataFrame, percentage: float):
	"""Oblicza cegiełki Renko na podstawie historycznych danych cenowych.
	:param historic_tickers: DataFrame zawierający co najmniej kolumnę 'price'.
	:param percentage: Procentowy rozmiar cegiełki wyrażony jako ułamek, np. 0.005 dla 0.5%.
	:return:
	"""

	np_price = historic_tickers['price'].to_numpy()
	renko_chart = []
	if not renko_chart:
		renko_chart.append({'cena': np_price[0], 'kierunek': 'brak'})

	up_cont = percentage + 1
	up_reversal = (1 - (2 * percentage))
	down_cont = 1 - percentage
	down_reversal = 2 * percentage + 1

	for current_price in np_price:
		last_brick = renko_chart[-1]
		last_price = last_brick['cena']
		last_direction = last_brick['kierunek']

		if last_direction == 'up':
			req_for_up_continuation = last_price * up_cont
			req_for_up_reversal = last_price * up_reversal

			if current_price >= req_for_up_continuation:
				renko_chart.append({'cena': current_price, 'kierunek': 'up'})

			elif current_price <= req_for_up_reversal:
				renko_chart.append({'cena': current_price, 'kierunek': 'down'})

		elif last_direction == 'down':
			req_for_down_continuation = last_price * down_cont
			req_for_down_reversal = last_price * down_reversal

			if current_price <= req_for_down_continuation:
				renko_chart.append({'cena': current_price, 'kierunek': 'down'})

			elif current_price >= req_for_down_reversal:
				renko_chart.append({'cena': current_price, 'kierunek': 'up'})

		elif last_direction == 'brak':
			wzrost = last_price * up_cont
			spadek = last_price * down_cont
			if current_price >= wzrost:
				renko_chart.append({'cena': current_price, 'kierunek': 'up'})

			elif current_price <= spadek:
				renko_chart.append({'cena': current_price, 'kierunek': 'down'})

	renko_df = pd.DataFrame(renko_chart)