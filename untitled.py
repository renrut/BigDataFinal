import pandas as pd

ft_df = pd.read_csv('data/season_stats_regular_season_with_ft.csv')
df = pd.read_csv('data/combo_stats_regular_season.csv')

col = ft_df['FTHELP']

df['FTHELP'] = col

df.to_csv('data/combo_stats_regular_season.csv',index=False)