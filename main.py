from src.logic import RenkoCalculator
from src.utils import get_root, get_file_name
from src.connections import DatabaseHandler
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np
import os


root = get_root()
hist_tickers_dir = f'{root}/Data/Ticker/Historic'

which_one = input('Which one script to run (1-n):')
if which_one == '1':
	market_type = input('Which type of market you want to run (spot or futures):')
	symbol = input('Which symbol do you want to run (eg. SUIUSDT):')
	start_year = int(input('From which year do you want to run (eg. 2024):'))
	end_year = int(input('To which year do you want to run (eg. 2025):'))
	start_month = int(input('From which month do you want to run (01-12):'))
	end_month = int(input('To which month do you want to run (01-12):'))

	file_list = get_file_name(symbol, start_year, end_year, start_month, end_month)
	total_files = len(file_list)
	print(f'Total files: {total_files}')

	print('Connecting to database...')
	try:
		db = DatabaseHandler()
		print('Connection established...')
	except Exception as e:
		print(f'Eroor with connection: {e}')
		exit()

	for index, file in enumerate(file_list):
		temp_df = pd.read_csv(f'{hist_tickers_dir}/{market_type}/{file}', usecols=['time', 'price', 'qty', 'is_buyer_maker'], chunksize=50000)
		temp_df['symbol'] = symbol
		db.append_df(temp_df, "trades")
		print(f'{index}/{total_files}')