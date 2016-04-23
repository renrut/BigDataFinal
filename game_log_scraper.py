import time
import os
import sys
import pandas as pd
import requests

reg = []
play = []

for year in range(1996,2016):
	second_half = ''
	if year<1999:
		second_half = str(year+1-1900)
	elif year<2009:
		second_half = '0'+str(year+1-2000)
	else:
		second_half = str(year+1-2000)

	season = str(year)+"-"+second_half
	requestReg = "http://stats.nba.com/stats/leaguegamelog?Counter=1000&Direction=DESC&LeagueID=00&PlayerOrTeam=T&Season="+season+"&SeasonType=Regular+Season&Sorter=PTS"
	requestPlayoff = "http://stats.nba.com/stats/leaguegamelog?Counter=1000&Direction=DESC&LeagueID=00&PlayerOrTeam=T&Season="+season+"&SeasonType=Playoffs&Sorter=PTS"
	
	url = "/usr/bin/open -a '/Applications/Google Chrome.app' '" + requestReg + "'"
	os.system(url)
	url = "/usr/bin/open -a '/Applications/Google Chrome.app' '" + requestPlayoff + "'"
	os.system(url)

	time.sleep(5)
	
	responseReg = requests.get(requestReg, timeout=20)
	dataReg = responseReg.json()['resultSets'][0]['rowSet']
	headersReg = responseReg.json()['resultSets'][0]['headers']

	responsePlay = requests.get(requestPlayoff, timeout=20)
	dataPlay = responsePlay.json()['resultSets'][0]['rowSet']
	headersPlay = responsePlay.json()['resultSets'][0]['headers']

	reg.append(pd.DataFrame(dataReg, columns=headersReg))
	play.append(pd.DataFrame(dataPlay, columns=headersPlay))

	print str(year)+".....done"
	# print output

pd.concat(reg).to_csv('data/game_logs_regular_season.csv')
pd.concat(play).to_csv('data/game_logs_playoffs.csv')
