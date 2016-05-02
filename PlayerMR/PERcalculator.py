import pandas as pd

data = pd.read_csv("data/combo_stats_regular_season.csv")
playerDF = pd.read_csv('data/player_stats_regular_season.csv')

# populate dictionaries on the fly to speed up calculations
pace_dict = {}
lg_aPER_dict = {}
game_dict = {}

def get_lg_avg(stat,year):
	if year not in game_dict:
		TG = data[data['SEASON_ID']==year]['GP'].mean()
		game_dict[year] = TG
	else:
		TG = game_dict[year]
	return TG*data.loc[data['SEASON_ID'] == year, stat].mean()

def get_player_aPER(player,year,GP):

	factor = (2.0/3) - (0.5 * (get_lg_avg('AST',year)/get_lg_avg('FGM',year))) / (2*(get_lg_avg('FGM',year) / get_lg_avg('FTM',year)))

	VOP = get_lg_avg('PTS',year)/(get_lg_avg('FGA',year)-get_lg_avg('OREB',year)+get_lg_avg('TOV',year) + (0.44*get_lg_avg('FTA',year)))

	DRB_per = get_lg_avg('DREB',year) / get_lg_avg('REB',year)


	curTeamSeason = data[data['SEASON_ID']==year]
	curTeamSeason = curTeamSeason[curTeamSeason['TEAM_ID']==player['TEAM_ID']]
	ast_FG = curTeamSeason['AST']/curTeamSeason['FGM']
	ast_FG = ast_FG.tolist()[0]
	if player.MIN == 0:
		minutes = 0.1
	else:
		minutes = player.MIN
	uPER = (1.0/(GP*minutes)) \
			* (GP*player.FG3M \
			+ (2.0/3) * GP*player.AST \
			+ (2.0 - factor * ast_FG) * GP*player.FGM \
			+ (GP*player.FTM * 0.5 * (1 + (1 - ast_FG) + (2.0/3) * ast_FG)) \
			- VOP * GP*player.TOV \
			- VOP * DRB_per * (GP*player.FGA - GP*player.FGM) \
			- VOP * 0.44 * (0.44 + (0.56 * DRB_per)) * (GP*player.FTA - GP*player.FTM) \
			+ VOP * (1 - DRB_per) * (GP*player.REB - GP*player.OREB) \
			+ VOP * DRB_per * GP*player.OREB \
			+ VOP * GP*player.STL \
			+ VOP * DRB_per * GP*player.BLK \
			- GP*player.PF * ((get_lg_avg('FTM',year)/get_lg_avg('PF',year))-0.44 * (get_lg_avg('FTM',year)/get_lg_avg('PF',year)) * VOP))

	if year not in pace_dict:		
		lg_pace = data[data['SEASON_ID']==year]['PACE'].mean()
		team_pace = data[data['SEASON_ID']==year]
		team_pace = team_pace[team_pace['TEAM_ID']==player['TEAM_ID']]['PACE'].mean()
		pace_adj = lg_pace/team_pace
		pace_dict[year] = pace_adj
	else:
		pace_adj = pace_dict[year]

	return pace_adj * uPER

def get_lg_aPER(year,games):
	if year not in lg_aPER_dict:
		player_aPERs=[]
		players = playerDF[playerDF['SEASON_ID']==year]
		for index, row in players.iterrows():
			minutes = row['MIN']
			player_aPERs.append(minutes * get_player_aPER(row, year, games))
		lg_aPER_dict[year] = sum(player_aPERs) / players['MIN'].sum()
		print players['MIN'].sum()
	return lg_aPER_dict[year]


for index, row in playerDF.iterrows():
	year = row['SEASON_ID']
	games = row['GP']
	player_aPER = get_player_aPER(row,year,games)
	lg_aPER = get_lg_aPER(year, games)
	PER = player_aPER*(15/lg_aPER)
	playerDF.loc[index, 'PER'] = PER

playerDF.to_csv("data/player_stats_regular_season.csv", index=False)
