import pandas as pd
from operator import add
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold, PredefinedSplit
year = 1998

squads = {
	1996: ["Atlanta Hawks","Boston Celtics","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Vancouver Grizzlies","Washington Bullets"],
	1997: ["Atlanta Hawks","Boston Celtics","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Vancouver Grizzlies","Washington Wizards"],
	1998: ["Atlanta Hawks","Boston Celtics","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Vancouver Grizzlies","Washington Wizards"],
	1999: ["Atlanta Hawks","Boston Celtics","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Vancouver Grizzlies","Washington Wizards"],
	2000: ["Atlanta Hawks","Boston Celtics","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Vancouver Grizzlies","Washington Wizards"],
	2001: ["Atlanta Hawks","Boston Celtics","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2002: ["Atlanta Hawks","Boston Celtics","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2003: ["Atlanta Hawks","Boston Celtics","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2004: ["Atlanta Hawks","Boston Celtics","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2005: ["Atlanta Hawks","Boston Celtics","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2006: ["Atlanta Hawks","Boston Celtics","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2007: ["Atlanta Hawks","Boston Celtics","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Seattle SuperSonics","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2008: ["Atlanta Hawks","Boston Celtics","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2009: ["Atlanta Hawks","Boston Celtics","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2010: ["Atlanta Hawks","Boston Celtics","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2011: ["Atlanta Hawks","Boston Celtics","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Jersey Nets","New Orleans Hornets","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2012: ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Hornets","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2013: ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2014: ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"],
	2015: ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]
}

mod = 0
for i in range(2014,year,-1):
	mod += len(squads[i])
print mod
squad = squads[year]
amt = len(squad)

# 0SEASON_ID,1TEAM_ID,2TEAM_NAME,3GP,4W,5L,6W_PCT,7MIN,8FGM,9FGA,10FG_PCT,11FG3M,12FG3A,13FG3_PCT,
# 14FTM,15FTA,16FT_PCT,17OREB,18DREB,19REB,20AST,21TOV,22STL,23BLK,24BLKA,25PF,26PTS,27PLUS_MINUS
def load_teams():
	df = pd.read_csv('data/season_stats_regular_season.csv')

	teams = []
	indices_to_use = [0,1,2,3,4,5,6,10,13,16,17,18,20,21,22,23,25,27]
	for index, row in df.iterrows():
		teams.append([row.tolist()[x] for x in indices_to_use])
	return teams[:-30]


# TEAM_ID, SEASON_ID, champs
def load_champs():
	df = pd.read_csv('data/champs.csv')

	champs = {}
	for index, row in df.iterrows():
		line = row.tolist()
		team = line[0]
		year = line[1]
		if line[2]==1.0:
			champs[(team, year)] = 1
	return champs


def load():
	return load_teams(), load_champs()


def create_input(teams):
	# don't want to cinlude SEASON_ID,TEAM_ID,TEAM_NAME,GP,W,L in predicition
	SKIP = 6
	WIDTH = len(teams[0]) - SKIP
	X = scipy.zeros((len(teams), WIDTH))
	for i in range(0, len(teams)):
		for j in range(SKIP,len(teams[0])):
			X[i, j-SKIP] = teams[i][j] if teams[i][j] != '' else 0
	return X


def create_output(teams, champs):
	Y = scipy.zeros(len(teams))
	for i in range(0, len(teams)):
		year = teams[i][0]
		team = teams[i][1]
		if (team, year) in champs:
			Y[i] = 1
	print 'Number of champs', sum(Y)
	return Y


def test_classifier(clf, X, Y):
	folds = StratifiedKFold(Y, 18)
	aucs = []
	for train, test in folds:

		clf.fit(X[train], Y[train])
		prediction_prob = clf.predict_proba(X[test])
		prediction = clf.predict(X[test])
		aucs.append(roc_auc_score(Y[test], prediction_prob[:, 1]))
	print clf.__class__.__name__, aucs, numpy.mean(aucs)


def main():
	teams, champs = load()
	X = create_input(teams)
	Y = create_output(teams, champs)
	# to explicitly define what are the test and train sets
	ps = PredefinedSplit(test_fold=([-1]*(len(teams)-amt-mod)+[0]*amt+[-1]*(mod)))
	resSGD = scipy.zeros(amt)
	sims = 1000
	for train_index, test_index in ps:
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = Y[train_index], Y[test_index]

		for i in range(0,sims):
			# see which classifier predicts what victor
			
			clf = linear_model.SGDClassifier(loss='log')
			clf.fit(X_train, y_train)
			cur = clf.predict(X_test)
			resSGD = map(add, resSGD, cur)

	print "SGD Classifier"
	resSGD = numpy.true_divide(resSGD, sims)
	for i in range(0,amt):
		print str(squad[i])+": "+str(round(100*resSGD[i]/sum(resSGD), 1))
	print "\n\n"

	clf = linear_model.SGDClassifier(loss='log')
	test_classifier(clf, X, Y)

	clf = GaussianNB()
	test_classifier(clf, X, Y)

	clf = RandomForestClassifier(n_estimators=10, max_depth=10)
	test_classifier(clf, X, Y)


if __name__ == '__main__':
	main()