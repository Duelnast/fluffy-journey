from src.utils import get_root
from src.connections import DatabaseHandler
import pandas as pd
import numpy as np
import pathlib as Path
import re
import os

root = get_root()

def last_file_number(file_path: Path):
	file_path.mkdir(parents=True, exist_ok=True)

	highest_number = 1
	for file in file_path.iterdir():
		match = re.match(r'(\d+)_.*\.pkl', file.name)
		if match:
			file_number = int(match.group(1))
			if file_number > highest_number:
				highest_number = file_number
		else:
			continue
	return highest_number

def db_to_pickle():
	pair = str(input('Which pair do you want to run (eg. SUIUSDT):'))
	pair = pair.upper()
	learning_data_path = root / "Data" / "Learning" / pair
	train_data_path = learning_data_path / "Train"
	valid_data_path = learning_data_path / "Validation"
	test_data_path = learning_data_path / "Test"
	last_file = last_file_number(train_data_path)

	print('Connecting to database...')
	db = DatabaseHandler()
	print('Connection established')
	with db.engine.connect() as connection:
		streaming_connection = connection.execution_options(stream_results=True)
		select_statement = f'SELECT time, open, high, low, close, volume, direction FROM futures_renko_percentage WHERE symbol = %(symbol_val)s ORDER BY time ASC'
		print('Reading data...')
		db_df = db.read_db(connection, 'futures_renko_percentage', pair, select_statement)

		for index, data_chunk in enumerate(db_df, start=last_file):
			print(f'Writing chunk {index}...')
			train_file = f'{index:02d}_train.pkl'
			valid_file = f'{index:02d}_validation.pkl'
			test_file = f'{index:02d}_test.pkl'

			train_set = data_chunk.iloc[0:200001]
			valid_set = data_chunk.iloc[200001:300001]
			test_set = data_chunk.iloc[300001:]

			train_set.to_pickle(f'{train_data_path}/{train_file}')
			print(f'Saved {train_file}')

			valid_set.to_pickle(f'{valid_data_path}/{valid_file}')
			print(f'Saved {valid_file}')

			test_set.to_pickle(f'{test_data_path}/{test_file}')
			print(f'Saved {test_file}')