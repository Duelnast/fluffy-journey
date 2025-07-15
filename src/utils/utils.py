from pathlib import Path
import pandas as pd

def get_root() -> Path:
	return Path(__file__).parent.parent.parent

def get_file_name(symbol: str, start_year: int, end_year: int, start_month: int, end_month: int):
	start_date = f'{start_year}-{start_month}-01'
	end_date = f'{end_year}-{end_month}-01'
	date_range = pd.date_range(start_date, end_date, freq="MS")

	data_list = []

	for date in date_range:
		year = date.year
		month = date.month
		if month < 10:
			true_month = "0" + str(month)
		else:
			true_month = month
		file_name = f'{symbol}-trades-{year}-{true_month}.csv'
		data_list.append(file_name)
	return data_list