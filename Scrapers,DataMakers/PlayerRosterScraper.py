import csv
import sys
import os
import time
from selenium import webdriver

def sleeep(x):
	print "Sleeping " + str(x) + " seconds"
	time.sleep(x)

#Basketball-Reference Scraper
#Get team extensions to generate urls
teamabrev = []
abrevdict = {}
URLlist = []
count = 30
year = sys.argv[1]
user = "yourusernamehere"
path = os.getcwd()

with open('data/br_teamid.csv','rb') as fi:
	reader = csv.reader(fi)
	for row in reader:
		#append each team abbreviation to the list
		teamabrev.append(row[3])
		#adding a list of alternate id's to dict
		abrevdict[row[3]] = []
		if row[4] != 'null':
			x = abrevdict[row[3]]
			x.append(row[4])
			abrevdict[row[3]] = x
		if row[5] != 'null':
			x = abrevdict[row[3]]
			x.append(row[5])
			abrevdict[row[3]] = x

#remove title
teamabrev.pop(0)
#hacky cases added as I moved back in time since team abbreviations changed.
teamabrev.append("SEA")
teamabrev.append("NOK")

#generate list of URLs
teamabrev = sorted(teamabrev)
for team in teamabrev:
	URLlist.append("http://www.basketball-reference.com/teams/"+team+"/"+str(year)+".html")

driver = webdriver.Chrome()
#download the csvs!
print teamabrev

for url in URLlist:
	count = count - 1
	print (30 - count)
	print "Getting " + url
	driver.get(url)
	try:
		driver.execute_script("sr_download_data('totals');")
		driver.get(url)
		driver.execute_script("sr_download_data('roster');")
	except Exception, e:
		print "Couldn't get " + url + " id may have changed."


#Move into data folder
name = "/Users/"+name+"/Downloads/"
moveroster = path + "/BigDataFinal/data/PlayerRosters"
movetotals = path + "/BigDataFinal/data/data/PlayerTotals"

for i in os.listdir(name):
    if "roster" in i: 
        os.rename(name + i, moveroster + i)
    elif "total" in i:
    	os.rename(name + i, movetotals + i)
    else:
        continue
