import time
import os
import sys
import pandas as pd
import requests

reg = []
df = pd.read_csv('data/season_stats_regular_season.csv')

for index, row in df.iterrows():
	year = row.SEASON_ID - 40000
	second_half = ''
	if year<1999:
		second_half = str(year+1-1900)
	elif year<2009:
		second_half = '0'+str(year+1-2000)
	else:
		second_half = str(year+1-2000)

	season = str(year)+"-"+second_half
	TeamID = row.TEAM_ID
	print str(row.TEAM_ID)+", "+season
	requestReg = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season="+season+"&SeasonSegment=&SeasonType=Regular+Season&TeamID="+str(TeamID)+"&VsConference=&VsDivision="
	
	url = "/usr/bin/open -a '/Applications/Google Chrome.app' '" + requestReg + "'"
	os.system(url)

	time.sleep(3)
	
	responseReg = requests.get(requestReg, timeout=20)
	try:
		dataReg = responseReg.json()['resultSets'][1]['rowSet']
		headersReg = responseReg.json()['resultSets'][1]['headers']
	except:
		try:
			dataReg = responseReg.json()['resultSets'][1]['rowSet']
			headersReg = responseReg.json()['resultSets'][1]['headers']
		except:
			try:
				dataReg = responseReg.json()['resultSets'][1]['rowSet']
				headersReg = responseReg.json()['resultSets'][1]['headers']
			except:
				try:
					dataReg = responseReg.json()['resultSets'][1]['rowSet']
					headersReg = responseReg.json()['resultSets'][1]['headers']
				except:
					try:
						dataReg = responseReg.json()['resultSets'][1]['rowSet']
						headersReg = responseReg.json()['resultSets'][1]['headers']
					except:
						pass
					pass
				pass
			pass
		pass
	regDF = pd.DataFrame(dataReg, columns=headersReg)
	regDF.insert(0, "TEAM_ID", TeamID)
	regDF.insert(0, "SEASON_ID", year+40000)
	reg.append(regDF)

	print str(year)+".....done"
	# print output

pd.concat(reg).to_csv('data/player_stats_regular_season.csv',index=False)

