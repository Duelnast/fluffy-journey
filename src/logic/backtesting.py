import vectorbt as vbt
import pandas as pd
import numpy as np
from src.utils import get_root

root = get_root()
renko_df = pd.read_csv(f"{root}/Data/Chart/Renko/SUIUSDT_renko.csv")

sygnal_numeryczny = pd.Series(np.where(renko_df['kierunek'] == 'up', 1, -1), name = 'Sygnal')
df_sygnal = pd.DataFrame(sygnal_numeryczny)

zmiana_kierunku = df_sygnal['Sygnal'] != df_sygnal['Sygnal'].shift(1)
id_bloku = zmiana_kierunku.cumsum()

df_sygnal['Czy zmiana?'] = zmiana_kierunku
df_sygnal['ID Bloku'] = id_bloku
df_sygnal['Licznik'] = df_sygnal.groupby('ID Bloku')['Sygnal'].cumsum()
np_licznik = df_sygnal['Licznik'].to_numpy()

df_sygnal.to_csv(f"{root}/Data/Chart/Renko/SUIUSDT_renko2.csv")

long_entries = (np_licznik == 5)
short_entries = (np_licznik == -5)

long_exits = (np_licznik == -1)
short_exits = (np_licznik == 1)


portfolio = vbt.Portfolio.from_signals(
    close = renko_df['cena'],
    entries = long_entries,
    exits = long_exits,
    short_entries = short_entries,
    short_exits = short_exits,
    freq = '1s',
    fees = 0.0006,
    init_cash= 4000,
)

print(portfolio.stats())
