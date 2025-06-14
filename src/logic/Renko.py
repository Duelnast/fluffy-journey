import pandas as pd
import numpy as np
from src.utils import get_root

root = get_root()
potrzebne_kolumny = ['price']

historic_tickers = pd.read_csv(f'{root}/Data/Ticker/Historic/Futures/SUI_USDT/SUIUSDT-trades-2024-12.csv', usecols = potrzebne_kolumny)
ceny_numpy = historic_tickers['price'].to_numpy()

renko_chart = []
if not renko_chart:
	renko_chart.append({'cena': ceny_numpy[0], 'kierunek': 'brak'})

print(renko_chart)
bazowy_procent_zmiany = 0.005
procent_zmiany_trendu_wzrostowego = bazowy_procent_zmiany + 1
odwrocenie_trendu_wzrostowego = (1 - (2 * bazowy_procent_zmiany))
procent_zmiany_trendu_spadkowego = 1 - bazowy_procent_zmiany
odwrocenie_trendu_spadkowego = 2 * bazowy_procent_zmiany + 1

for aktualna_cena in ceny_numpy:
	ostatnia_cegielka = renko_chart[-1]
	poprzednia_cena = ostatnia_cegielka['cena']
	kierunek_ostatniej_cegielki = ostatnia_cegielka['kierunek']

	if kierunek_ostatniej_cegielki == 'up':
		prog_wzrostowy_kontynuacji = poprzednia_cena * procent_zmiany_trendu_wzrostowego
		prog_wzrostowy_odwrocenia = poprzednia_cena * odwrocenie_trendu_wzrostowego

		if aktualna_cena >= prog_wzrostowy_kontynuacji:
			renko_chart.append({'cena': round(prog_wzrostowy_kontynuacji, 4), 'kierunek': 'up'})

		elif aktualna_cena <= prog_wzrostowy_odwrocenia:
			renko_chart.append({'cena': round(prog_wzrostowy_odwrocenia, 4), 'kierunek': 'down'})

	elif kierunek_ostatniej_cegielki == 'down':
		prog_spadkowy_kontynuacji = poprzednia_cena * procent_zmiany_trendu_spadkowego
		prog_spadkowy_odwrocenia = poprzednia_cena * odwrocenie_trendu_spadkowego

		if aktualna_cena <= prog_spadkowy_kontynuacji:
			renko_chart.append({'cena': round(prog_spadkowy_kontynuacji, 4), 'kierunek': 'down'})

		elif aktualna_cena >= prog_spadkowy_odwrocenia:
			renko_chart.append({'cena': round(prog_spadkowy_odwrocenia, 4), 'kierunek': 'up'})

	elif kierunek_ostatniej_cegielki == 'brak':
		wzrost = poprzednia_cena * procent_zmiany_trendu_wzrostowego
		spadek = poprzednia_cena * procent_zmiany_trendu_spadkowego
		if aktualna_cena >= wzrost:
			renko_chart.append({'cena': round(wzrost, 4), 'kierunek': 'up'})

		elif aktualna_cena <= spadek:
			renko_chart.append({'cena': round(spadek, 4), 'kierunek': 'down'})

df = pd.DataFrame(renko_chart)
print(df)