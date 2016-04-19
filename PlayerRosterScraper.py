import csv
import os
import time
from selenium import webdriver

def sleeep(x):
	print "Sleeping " + str(x) + " seconds"
	time.sleep(x)

#Basketball-Reference Scraper
#Get team extensions to generate urls
teamabrev = []
URLlist = []
year = "2016"

with open('data/team_id.csv','rb') as fi:
	reader = csv.reader(fi)
	for row in reader:
		#append each team abbreviation to the list
		teamabrev.append(row[3])
teamabrev.append("NJN")

#remove title
teamabrev.pop(0)

#generate list of URLs
for team in teamabrev:
	URLlist.append("http://www.basketball-reference.com/teams/"+team+"/"+year+".html")


driver = webdriver.Chrome()
#download the csvs!
print teamabrev
for url in URLlist[9:]:
	driver.get(url)
	try:
		driver.execute_script("sr_download_data('totals');")
		sleeep(1)
		driver.get(url)
		driver.execute_script("sr_download_data('roster');")
		sleeep(1)
	except Exception, e:
		print url


#Move into our folder
for team in teamabrev:
	name1 = "teams_"+ team +"_2016_roster.csv"
	name2 = "teams_"+ team +"_2016_totals.csv"
	try:
		os.rename("/Users/turnerstrayhorn/Downloads/"+name1, "/Users/turnerstrayhorn/Turner/School/BigData/BigDataFinal/data/Players/"+name1)
		os.rename("/Users/turnerstrayhorn/Downloads/"+name2, "/Users/turnerstrayhorn/Turner/School/BigData/BigDataFinal/data/Players/"+name2)
	except:
		print team + " not found."