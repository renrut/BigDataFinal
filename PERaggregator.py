import pandas as pd

players = pd.read_csv('data/player_stats_regular_season.csv')
data = pd.read_csv('data/combo_stats_regular_season.csv')

for index, row in data.iterrows():
	team = row['TEAM_ID']
	year = row['SEASON_ID']

	team_players = players[players['TEAM_ID']==team]
	team_players = team_players[team_players['SEASON_ID']==year]
	vals = []
	for index2, player in team_players.iterrows():
		vals.append(player['MIN']*player['PER'])
	data.loc[index, 'TEAM_PER'] = (sum(vals)/team_players['MIN'].sum()) - 15

data.to_csv("data/combo_stats_regular_season.csv", index=False)