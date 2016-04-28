import os
import csv


# This takes each player roster and compiles it into one large team roster
# It assumes the roster files are called "teams_ABR_YEAR_roster.csv"
# The script appends the team abreviation and the year to the end of each row
ap = open('data/allteamstotals.csv','w')
g = csv.writer(ap, delimiter=',')
name = os.getcwd()+"/data/PlayerTotals/"
for i in os.listdir(name):
    if "totals" in i:

    	#get abrev from i
    	abrev = i[6:9]
    	print abrev
    	#get year from i
    	year = i[10:14]
    	print year
    	#append year and abrev to row
    	with open(name+i,'rb') as fi:
			reader = csv.reader(fi)
			for row in reader:
				row.append(abrev)
				row.append(year)
				g.writerow(row)

    else:
        continue
ap.close()
