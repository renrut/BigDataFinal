# import scrapy
import csv
import json
import urllib2
import time
import random
import os
import sys

teamlist = []

with open("data/team_id.csv", "rb") as csvfile:
     spamreader = csv.reader(csvfile)
     for row in spamreader:
         teamlist.append([row[3],row[0]])




# teamlist:
# [abbreviation, teamid]
teamlist = teamlist[1:]
# for team in teamlist:
# 	teamid = str(team[1])
# 	abrv = team[0]
# 	print "Team " + str(team)
fp = open('latedata.json', 'w')

for i in range(0,30):
	print teamlist[i]
	request = "http://stats.nba.com/stats/teamdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&TeamID="+teamlist[i][1]+"&VsConference=&VsDivision="
	# url = "/usr/bin/open -a '/Applications/Google Chrome.app' '" + request + "'"
	# os.system(url)
	data = urllib2.urlopen(request, timeout=5)
	output = json.loads(data.read())
	print output
	json.dump(output, fp)





	# try:
	# 	output = json.loads(data.read())

	# except:
	# 	print "ERROR 2" + teamid
	

	print "\n\n"
	# print output