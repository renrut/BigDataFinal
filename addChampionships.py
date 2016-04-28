import pandas as pd
import numpy

champs= {
	41996: 1610612741,
	41997: 1610612741,
	41998: 1610612759,
	41999: 1610612747,
	42000: 1610612747,
	42001: 1610612747,
	42002: 1610612759,
	42003: 1610612765,
	42004: 1610612759,
	42005: 1610612748,
	42006: 1610612759,
	42007: 1610612738,
	42008: 1610612747,
	42009: 1610612747,
	42010: 1610612742,
	42011: 1610612748,
	42012: 1610612748,
	42013: 1610612759,
	42014: 1610612744,
	42015: 0
}
year = 2014

data = pd.read_csv("data/combo_stats_regular_season.csv")

def get_lg_avg(stat):
	return data.loc[data['SEASON_ID'] == year+40000, stat].sum()

playerDF = pd.read_csv('data/PlayerTotals/teams_GSW_2015_totals.csv')
print playerDF

team_stats = playerDF.tail(1)

for index, row in playerDF.iterrows():
	print str(row.Player)
	factor = (2.0/3) - (0.5*(get_lg_avg('AST')/get_lg_avg('FGM')))/(2*(get_lg_avg('FGM')/get_lg_avg('FTM')))
	print factor
	VOP = get_lg_avg('PTS')/(get_lg_avg('FGA')-get_lg_avg('OREB')+get_lg_avg('TOV')+0.44*get_lg_avg('FTA'))
	print VOP
	DRB_per = (get_lg_avg('REB')-get_lg_avg('OREB')) / get_lg_avg('REB')
	print DRB_per
	ast_FG = team_stats['AST']/team_stats['FG']

	uPER = (1.0/row.MP) * \
			(row['3P'] + \
			(2.0/3) * row.AST + \
			(2.0 - factor * ast_FG) * row.FG + \
			(row.FT * 0.5 * (1 + (1 - ast_FG) + (2.0/3) * ast_FG)) - \
			(VOP * row.TOV) - \
			(VOP * DRB_per * (row.FGA - row.FG)) - \
			(VOP * 0.44 * (0.44 + (0.56 * DRB_per)) * (row.FTA - row.FT)) + \
			(VOP * (1 - DRB_per) * (row.TRB - row.ORB)) + \
			(VOP * DRB_per * row.ORB) + \
			(VOP * row.STL) + \
			(VOP * DRB_per * row.BLK) - \
			row.PF * ((get_lg_avg('FTM')/get_lg_avg('PF'))-0.44* (get_lg_avg('FTM')/get_lg_avg('PF')) * VOP))
	aPER = 93.9 * uPER
	print aPER
	print str(row.Player) + ": " + str(uPER)
#data.to_csv("data/combo_stats_regular_season.csv", index=False)

#new_df = pd.concat([data.TEAM_ID,data.SEASON_ID],axis=1)

#new_df['champs'] = numpy.zeros(len(data.index))
#for index, row in data.iterrows():
#	if champs[row['SEASON_ID']] == row['TEAM_ID']:
#		new_df.loc[index, 'champs'] = 1
#	else:
#		new_df.loc[index, 'champs'] = 0
#print new_df
#new_df.to_csv("data/champs.csv")