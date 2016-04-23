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
	TEAM_ID = 1000000001
	requestReg = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season="+season+"&SeasonSegment=&SeasonType=Regular+Season&TeamID="+TEAM_ID+"7&VsConference=&VsDivision="
	requestPlayoff = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season="+season+"&SeasonSegment=&SeasonType=Playoffs&TeamID="+TEAM_ID+"&VsConference=&VsDivision="
	
	url = "/usr/bin/open -a '/Applications/Google Chrome.app' '" + requestReg + "'"
	os.system(url)
	url = "/usr/bin/open -a '/Applications/Google Chrome.app' '" + requestPlayoff + "'"
	os.system(url)

	time.sleep(5)
	
	responseReg = requests.get(requestReg, timeout=20)
	dataReg = responseReg.json()['resultSets'][1]['rowSet']
	headersReg = responseReg.json()['resultSets'][1]['headers']

	responsePlay = requests.get(requestPlayoff, timeout=20)
	dataPlay = responsePlay.json()['resultSets'][1]['rowSet']
	headersPlay = responsePlay.json()['resultSets'][1]['headers']

	regDF = pd.DataFrame(dataReg, columns=headersReg)
	regDF.insert(0, "TEAM_ID",TEAM_ID)
	regDF.insert(0, "SEASON_ID", year+40000)
	playDF = pd.DataFrame(dataPlay, columns=headersPlay)
	playDF.insert(0, "TEAM_ID",TEAM_ID)
	playDF.insert(0, "SEASON_ID", year+40000)
	reg.append(regDF)
	play.append(playDF)

	print str(year)+".....done"
	# print output

pd.concat(reg).to_csv('data/season_stats_regular_season.csv')
pd.concat(play).to_csv('data/season_stats_playoffs.csv')