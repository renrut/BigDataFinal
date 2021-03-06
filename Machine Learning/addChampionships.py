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

data = pd.read_csv("data/season_stats_regular_season.csv")
data_adv = pd.read_csv("data/advanced_stats_regular_season.csv")
new_cols = ['OFF_RATING','DEF_RATING','NET_RATING','AST_PCT','AST_TO','AST_RATIO','OREB_PCT','DREB_PCT','REB_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','PACE','PIE']
for col in new_cols:
	data[col] = data_adv[col]
data.to_csv("data/combo_stats_regular_season.csv", index=False)

#new_df = pd.concat([data.TEAM_ID,data.SEASON_ID],axis=1)

#new_df['champs'] = numpy.zeros(len(data.index))
#for index, row in data.iterrows():
#	if champs[row['SEASON_ID']] == row['TEAM_ID']:
#		new_df.loc[index, 'champs'] = 1
#	else:
#		new_df.loc[index, 'champs'] = 0
#print new_df
#new_df.to_csv("data/champs.csv")