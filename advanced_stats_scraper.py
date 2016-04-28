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
	requestReg = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season="+season+"&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
	requestPlayoff = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season="+season+"&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
	
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

	regDF = pd.DataFrame(dataReg, columns=headersReg)
	regDF.insert(0, "SEASON_ID", year+40000)
	playDF = pd.DataFrame(dataPlay, columns=headersPlay)
	playDF.insert(0, "SEASON_ID", year+40000)
	reg.append(regDF)
	play.append(playDF)

	print str(year)+".....done"
	# print output

pd.concat(reg).to_csv('data/advanced_stats_regular_season.csv')
pd.concat(play).to_csv('data/advanced_stats_playoffs.csv')