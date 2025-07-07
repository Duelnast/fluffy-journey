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

	while True:
		print("""Available scripts:
		-Saving csv to db - type: 1
		-Reading data from db, calculating renko and saving to db - type: 2
		-Exit
		""")
		which_one = input('Which one script to run:')
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

		if which_one == '2':
			pair = input('Which pair do you want to run (eg. SUIUSDT):')
			percentage = float(input('Which renko brick percentage do you want (eg. 0.005 = 0.5%):'))

			print('Connecting to database...')

			db = DatabaseHandler()
			print('Connection established...')
			with db.engine.connect() as connection:
				streaming_connection = connection.execution_options(stream_results=True)
				print('Reading data...')
				db_df = db.read_db(connection,'ticker_trades_futures', pair)

				print('Calculating renko bricks...')
				renko_calculator = RenkoCalculator(percentage)

				for data_chunk in db_df:
					calculated_renko = renko_calculator.calculate(data_chunk)
					calculated_renko['brick_size_bp'] = percentage * 10000
					calculated_renko['symbol'] = pair
					print('Writing chunk of data...')
					db.append_df(calculated_renko, 'futures_renko_percentage')
					#renko_calculator.trim_history()

				print('Done')

		if which_one.lower() == 'exit':
			break
