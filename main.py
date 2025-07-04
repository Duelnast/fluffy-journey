from src.logic import RenkoCalculator
from src.utils import get_root, get_file_name
from src.connections import DatabaseHandler
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
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
		full_file_list = [f'{hist_tickers_dir}/{market_type}/{file}' for file in file_list]
		total_files = len(file_list)
		print(f'Total files: {total_files}')

		print('Connecting to database...')
		try:
			db = DatabaseHandler()
			print('Connection established...')
		except Exception as e:
			print(f'Error with connection: {e}')
			exit()

		def saving_into_db(file_path):
			try:
				for df_chunk in pd.read_csv(file_path, usecols=['time', 'price', 'qty', 'is_buyer_maker'], chunksize=500000):
					df_chunk['symbol'] = symbol
					db.append_df(df_chunk, "ticker_trades_futures")

				print(f'Thread {os.getpid()}: finished file {os.path.basename(file_path)}')
			except Exception as e:
				print(f'Error with the processing file {os.path.basename(file_path)}: {e}')

		with ThreadPoolExecutor(max_workers=16) as executor:
			executor.map(saving_into_db, full_file_list)

		print('Finished! All files saved in database.')