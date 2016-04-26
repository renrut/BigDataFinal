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
year = "2008"

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

#generate list of URLs
teamabrev = sorted(teamabrev)
for team in teamabrev:
	URLlist.append("http://www.basketball-reference.com/teams/"+team+"/"+year+".html")

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


#Move into our folder
for team in teamabrev:
	name1 = "teams_"+ team +"_"+year+"_roster.csv"
	name2 = "teams_"+ team +"_"+year+"_totals.csv"
	try:
		os.rename("/Users/turnerstrayhorn/Downloads/"+name1, "/Users/turnerstrayhorn/Turner/School/BigData/BigDataFinal/data/Players/"+name1)
		os.rename("/Users/turnerstrayhorn/Downloads/"+name2, "/Users/turnerstrayhorn/Turner/School/BigData/BigDataFinal/data/Players/"+name2)
	except:
		print team + " not found. Trying alternatives."
		for x in abrevdict[team]:
				name1 = "teams_"+ x +"_"+year+"_roster.csv"
				name2 = "teams_"+ x +"_"+year+"_totals.csv"
				try:
					os.rename("/Users/turnerstrayhorn/Downloads/"+name1, "/Users/turnerstrayhorn/Turner/School/BigData/BigDataFinal/data/Players/"+name1)
					os.rename("/Users/turnerstrayhorn/Downloads/"+name2, "/Users/turnerstrayhorn/Turner/School/BigData/BigDataFinal/data/Players/"+name2)
				except:
					print x + " not found."