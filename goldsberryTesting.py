#!/usr/bin/python

import requests
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import goldsberry
import shotMethods

print "Enter player"
playerName = raw_input(">> ")
print "Enter year (in format yyyy-yy (e.g. 2015-16))"
year = raw_input(">> ")
lastFirst = ', '.join(reversed(playerName.split(' ')))
playerList = goldsberry.PlayerList()
playerList.SET_parameters(season=year)
playerList.GET_raw_data()
players = pd.DataFrame(playerList.players())
playerID = players[players.DISPLAY_LAST_COMMA_FIRST == lastFirst].PERSON_ID

shot_chart = goldsberry.player.shot_chart(playerID)
shot_chart.SET_parameters(season=year)
shot_chart.GET_raw_data()
shots = shot_chart.chart()
shot_df = pd.DataFrame([item.values() for item in shots], columns=shots[0].keys())
leagueAvgs = shot_chart.leagueaverage()
leagueAvg_df = pd.DataFrame([item.values() for item in leagueAvgs], columns=leagueAvgs[0].keys())

cmap = shotMethods.get_cmap()

def getFgStr(row):
	return row.SHOT_ZONE_BASIC+'-'+row.SHOT_ZONE_AREA+': '+row.SHOT_ZONE_RANGE

def getLgAvgZones(df):
	zoneAvgs = {}
 	for index, row in df.iterrows():
 		zoneAvgs[getFgStr(row)] = row.FG_PCT
 	return zoneAvgs

def getPlayerZones(df, lgAvgs):
	zoneAvgLists = {}
	for index, row in df.iterrows():
		zoneAvgLists.setdefault(getFgStr(row), []).append(row.SHOT_MADE_FLAG)
	zoneAvgs={}
	for z in lgAvgs:
		if z in zoneAvgLists:
			zoneAvgs[z] = sum(zoneAvgLists[z])/float(len(zoneAvgLists[z]))
		else:
			zoneAvgs[z] = 0
	return zoneAvgs

avgShotDict = getLgAvgZones(leagueAvg_df)
playerAverages = getPlayerZones(shot_df,avgShotDict)

shot_df['ZONE_AVG'] = [playerAverages[getFgStr(row)] for index, row in shot_df.iterrows()]

#1.07
#1.03
#0.98
#0.94
def compare(avgShots, playerShots):
	relativeShotDict = {}
	for zone in avgShots:
		if playerShots[zone]>avgShots[zone]*1.07:
			relativeShotDict[zone] = .9
		elif playerShots[zone]>avgShots[zone]*1.03:
			relativeShotDict[zone] = .7
		elif playerShots[zone]>avgShots[zone]*.97:
			relativeShotDict[zone] = .5
		elif playerShots[zone]>avgShots[zone]*.93:
			relativeShotDict[zone] = .3
		else:
			relativeShotDict[zone] = .1
	return relativeShotDict


meltedAvgs = compare(avgShotDict, playerAverages)
shot_df['ZONE_COLOR'] = [meltedAvgs[getFgStr(row)] for index, row in shot_df.iterrows()]

plt.figure(figsize=(11,9))

# plot the figure using matplotlib's hexbin plot methods
im = plt.hexbin(shot_df.LOC_X,shot_df.LOC_Y, C=shot_df.ZONE_COLOR, marginals=False,
		   bins='log', cmap=cmap, gridsize=75, edgecolors='#152435')

# draw the court lines on the current plot
shotMethods.draw_court()
#shotMethods.get_player_portrait(playerID)

# set the limits of the court to display the half court
plt.ylim([424.5,-49.5])
plt.xlim([-252,252])

# take off axis tick marks, no use for them in this context
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

# add a title
plt.title(playerName+' FGA \n'+year+' Reg. Season', fontsize=20, y=1.01)

# set the background color
plt.gca().set_axis_bgcolor('#152435')
plt.show()