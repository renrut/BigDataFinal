import time
import os
import sys
import pandas as pd
import requests

reg = []
for year in range(1996,2016):
	second_half = ''
	if year<1999:
		second_half = str(year+1-1900)
	elif year<2009:
		second_half = '0'+str(year+1-2000)
	else:
		second_half = str(year+1-2000)

	season = str(year)+"-"+second_half
	requestReg = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season="+season+"&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
	
	url = "/usr/bin/open -a '/Applications/Google Chrome.app' '" + requestReg + "'"
	os.system(url)

	time.sleep(4)
	
	responseReg = requests.get(requestReg, timeout=20)
	try:
		dataReg = responseReg.json()['resultSets'][0]['rowSet']
		headersReg = responseReg.json()['resultSets'][0]['headers']
	except:
		try:
			dataReg = responseReg.json()['resultSets'][0]['rowSet']
			headersReg = responseReg.json()['resultSets'][0]['headers']
		except:
			pass
		pass


	regDF = pd.DataFrame(dataReg, columns=headersReg)
	regDF.insert(0, "SEASON_ID", year+40000)
	reg.append(regDF)

	print str(year)+".....done"
	# print output

pd.concat(reg).to_csv('data/season_stats_regular_season.csv',index=False)







