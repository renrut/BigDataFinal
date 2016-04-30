import pandas as pd
from operator import add
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold, PredefinedSplit

# Base Stats
# Base + Team_PER
# FT
# Everything combined

# makes output correct year to year
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
indices = {
	'SEASON_ID':0,
	'TEAM_ID':1,
	'TEAM_NAME':2,
	'GP':3,
	'W':4,
	'L':5,
	'W_PCT':6,
	'MIN':7,
	'FGM':8,
	'FGA':9,
	'FG_PCT':10,
	'FG3M':11,
	'FG3A':12,
	'FG3_PCT':13,
	'FTM':14,
	'FTA':15,
	'FT_PCT':16,
	'OREB':17,
	'DREB':18,
	'REB':19,
	'AST':20,
	'TOV':21,
	'STL':22,
	'BLK':23,
	'BLKA':24,
	'PF':25,
	'PTS':26,
	'PLUS_MINUS':27,
	'OFF_RATING':28,
	'DEF_RATING':29,
	'NET_RATING':30,
	'AST_PCT':31,
	'AST_TO':32,
	'AST_RATIO':33,
	'OREB_PCT':34,
	'DREB_PCT':35,
	'REB_PCT':36,
	'TM_TOV_PCT':37,
	'EFG_PCT':38,
	'TS_PCT':39,
	'PACE':40,
	'PIE':41,
	'TEAM_PER':42
}

for year in squads:
	#year = 2015
	print "YEAR = "+str(year)

	# mod is used as basically a way to shift the position of the train and test sets. Has to be variable as
	# the amount of NBA teams isnt always 30
	mod = 0
	for i in range(2014,year,-1):
		mod += len(squads[i])
	squad = squads[year]
	# number of teams in the current year
	amt = len(squad)

	def load_teams():
		# read in data into Pandas DataFrame
		df = pd.read_csv('data/combo_stats_regular_season.csv')
		teams = []
		# self-descriptive. What these indices correspond to are listed above
		stats_to_use = ['SEASON_ID','TEAM_ID','TEAM_NAME','GP','W','L','W_PCT','FG_PCT','FG3_PCT',
						'FT_PCT','AST_TO','AST_PCT','STL','BLK','REB_PCT','NET_RATING','PLUS_MINUS','TEAM_PER']
		# converting every row into a list and then appending it to the input matrix stored into an array
		for index, row in df.iterrows():
			teams.append([row.tolist()[indices[x]] for x in stats_to_use])
		# for now ignore the most recent season as it screws up data of past years
		return teams[:-30]

	# TEAM_ID, SEASON_ID, champs
	def load_champs():
		# read champs data to Pandas DataFrame
		df = pd.read_csv('data/champs.csv')
		champs = {}
		# mark a (team, year) tuple as champions or not
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
		# for every team/season combination mark if champs or not
		Y = scipy.zeros(len(teams))
		for i in range(0, len(teams)):
			year = teams[i][0]
			team = teams[i][1]
			if (team, year) in champs:
				Y[i] = 1
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
		# the test_fold corresponds to the number of rows are going to be used for which:
		# either to be used for training only (-1) or to be used in a testing group (0)
		ps = PredefinedSplit(test_fold=([-1]*(len(teams)-amt-mod)+[0]*amt+[-1]*(mod)))
		resSGD = scipy.zeros(amt)
		# going to run a 1000 simulations
		sims = 1000
		for train_index, test_index in ps:
			# get X and Y test and train data
			X_train, X_test = X[train_index], X[test_index]
			y_train, y_test = Y[train_index], Y[test_index]
			for i in range(0,sims):
				clf = linear_model.SGDClassifier(loss='log')
				clf.fit(X_train, y_train)
				cur = clf.predict(X_test)
				#resSGD is a cumulation of all predicted winners in all simulations
				resSGD = map(add, resSGD, cur)
		print "SGD Classifier"
		# dividing wins for each team by the number of simulations
		playoffDF = pd.read_csv('data/season_stats_playoffs.csv')
		playoffDF = playoffDF.loc[playoffDF['SEASON_ID'] == 40000+year]
		resSGD = numpy.true_divide(resSGD, sims)
		for i in range(0,amt):
			if not any(playoffDF.TEAM_NAME == squad[i]):
				resSGD[i] = 0.0
		for i in range(0,amt):
			# normalize so its all out of 100%
			print str(squad[i])+": "+str(round(100*resSGD[i]/sum(resSGD), 1))
		print "\n\n"
		# different classifiers to test AUC
		clf = linear_model.SGDClassifier(loss='log')
		test_classifier(clf, X, Y)
		clf = GaussianNB()
		test_classifier(clf, X, Y)
		clf = RandomForestClassifier(n_estimators=10, max_depth=10)
		test_classifier(clf, X, Y)

	if __name__ == '__main__':
		main()