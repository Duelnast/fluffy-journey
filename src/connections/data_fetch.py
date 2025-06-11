from dotenv import load_dotenv
from pathlib import Path
import os
import ccxt
import pandas as pd
import numpy as np #ignore


load_dotenv() #ladowanie kluczy api
api_key1 = str(os.environ.get('bitget_api_key'))
secret_api_key1 = str(os.environ.get('bitget_secret_api_key'))
symbol1 = "SUI/USDT:USDT"
exchange1 = "bitget"
market_type1 = "FUTURES"

def fetching_trades(symbol: str, exchange_id: str, market_type: str, api_key: str, secret_api_key: str):
	#ustawienie gieldy oraz symbolu
	chosen_symbol = symbol
	chosen_exchange = getattr(ccxt, exchange_id)
	exchange = chosen_exchange({
		"apiKey": api_key,
		"secret": secret_api_key,
		"enableRateLimit": True
	})

	#pobranie historycznych transakcji oraz przetransformowanie jej do DataFrame z pandas
	trade = exchange.fetch_trades(chosen_symbol)
	trades = pd.DataFrame(trade)
	needed_df = trades[['datetime', 'price']]

	#przeksztalcenie nazwy symbolu tak by mozna bylo zapisac plik oraz zapisanie pliku
	first_name_change = chosen_symbol.replace('/', '_')
	second_name_change = first_name_change.replace(':', '_')
	correct_file_name = second_name_change.lower()

	#zdefiniowanie nazwy folderu
	if ":USDT" in first_name_change:
		folder_name = first_name_change.replace(':USDT', '')
	else:
		folder_name = first_name_change

	#zdefiniowanie sciezki folderu do zapisu pobranych danych i utworzenie brakujacego folderu
	desired_path = f"../../Data/{folder_name}/{market_type}/{correct_file_name}_tickers.csv"
	file_path = Path(desired_path)
	target_directory = file_path.parent
	target_directory.mkdir(parents = True, exist_ok = True)

	needed_df.to_csv(file_path, index = False)

	return trades

fetching_trades(symbol1, exchange1, market_type1, api_key1, secret_api_key1)