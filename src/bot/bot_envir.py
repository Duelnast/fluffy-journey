from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3 import PPO
from src.utils import get_root
import pandas as pd
import numpy as np
import gymnasium as gym
import time
import os
import gym_trading_env

def add_features(df: pd.DataFrame):
	df["feature_close"] = df["close"].pct_change()
	df["feature_open"] = df["open"] / df["close"]
	df["feature_high"] = df["high"] / df["close"]
	df["feature_low"] = df["low"] / df["close"]
	df["feature_volume"] = df["volume"] / df["volume"].rolling(7 * 24).max()
	df["feature_direction"] = np.where(df["direction"] == 'up', 1, -1)
	df.dropna(inplace=True)

	return df


def reward_function(history):
	return np.log(history["portfolio_valuation", -1] / history["portfolio_valuation", -2])  # log (p_t / p_t-1 )


if __name__ == "__main__":
	pair = "SUIUSDT"
	# str(input('Which pair do you want to run (eg. SUIUSDT):'))
	root = get_root()
	learning_data_path = root / "Data" / "Learning" / pair
	train_data_path = learning_data_path / "Train"
	valid_data_path = learning_data_path / "Validation"
	test_data_path = learning_data_path / "Test"

	env = gym.make(
		id="MultiDatasetTradingEnv",
		dataset_dir=f'{root}/Data/Learning/{pair}/Test/*.pkl',
		preprocess=add_features,
		windows=5,
		positions=[-1, -0.5, 0, 0.5, 1, 1.5, 2],
		initial_position=0,
		trading_fees=0.0006 / 100,
		borrow_interest_rate=0.0003 / 100,
		reward_function=reward_function,
		portfolio_initial_value=1000,
		verbose=0
	)
	start_time = time.monotonic()

	#Model parameters
	policy_kwargs = dict(
		net_arch=dict(pi=[256, 256], vf=[256, 256])
	) #number of neurons
	n_steps = 4096 #number of steps before model update
	batch_size = 64 #number of data "portion" used in one model update, must be lower than n_steps

	model = PPO("MlpPolicy", env, verbose=1, device="cpu")
	model.learn(total_timesteps=2000, progress_bar=True)
	model.save("PPO_" + pair)

	end_time = time.monotonic()
	duration = end_time - start_time
	print(f"Duration: {duration:.2f} seconds")