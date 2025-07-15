from dotenv import load_dotenv

import os
import sqlalchemy
import pandas as pd

load_dotenv()

class DatabaseHandler:
	def __init__(self):
		db_user = os.environ.get("DB_USER")
		db_password = os.environ.get("DB_PASS")
		db_host = os.environ.get("DB_HOST")
		db_port = os.environ.get("DB_PORT")
		db_name = os.environ.get("DB_NAME")

		db_connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

		try:
			self.engine = sqlalchemy.create_engine(db_connection_string)

		except Exception as e:
			print(f'Database connection failed: {e}')

	def append_df(self, df_to_save: pd.DataFrame, table_name: str):
		try:
			df_to_save.to_sql(table_name, con=self.engine, if_exists='append', index=False)

		except sqlalchemy.exc.OperationalError:
			print("Database connection failed")

	def read_db(self, connection, table_name: str, pair: str, select_statement: str):
		if select_statement == "":
			select_statement = f'SELECT time, price, qty FROM {table_name} WHERE symbol = %(symbol_val)s ORDER BY time ASC'
		else:
			select_statement = select_statement
		params_dict = {"symbol_val": pair}

		try:
			which_one = input("Chunked data? [y/n]")
			if which_one == 'y':
				chunk_size = input("Chunk size (default(or blank) = 400000): ")
				if chunk_size == 'default' or chunk_size == "":
					return pd.read_sql(select_statement, connection, params=params_dict, chunksize=400000)
				else:
					return pd.read_sql(select_statement, connection, params=params_dict, chunksize=int(chunk_size))
			elif which_one == 'n':
				return pd.read_sql(select_statement, connection, params=params_dict)
		except Exception as e:
			print(f"Database connection failed: {e}")