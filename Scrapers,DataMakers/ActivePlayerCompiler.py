import csv

# ActivePlayerCompiler
# This file takes all team csv files and places them into one file with their team abbreviation

#Basketball-Reference Scraper
#Get team extensions to generate urls
teamabrev = []
URLlist = []
year = "2016"

ap = open('data/allteams.csv','w')

with open('data/team_id_copy.csv','rb') as fi:
	reader = csv.reader(fi)
	for row in reader:
		#append each team abbreviation to the list
		teamabrev.append(row[3])
teamabrev = teamabrev[1:]
print teamabrev

g = csv.writer(ap, delimiter=',')

for team in teamabrev:
	name = "data/Players/teams_"+ team +"_2016_roster.csv"
	try:
		with open(name,'rb') as lists:
			reader = csv.reader(lists)
			for row in reader:
				row.append(team)
				g.writerow(row)

				#append each team abbreviation to the list
	except Exception, e:
		print e
ap.close()