import pandas as pd
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold, PredefinedSplit


# 0SEASON_ID,1TEAM_ID,2TEAM_NAME,3GP,4W,5L,6W_PCT,7MIN,8FGM,9FGA,10FG_PCT,11FG3M,12FG3A,13FG3_PCT,
# 14FTM,15FTA,16FT_PCT,17OREB,18DREB,19REB,20AST,21TOV,22STL,23BLK,24BLKA,25PF,26PTS,27PLUS_MINUS
def load_teams():
	df = pd.read_csv('data/season_stats_regular_season.csv')

	teams = []
	indices_to_use = [0,1,2,3,4,5,6,8,10,11,13,14,16,17,18,20,21,22,23,25,27]
	for index, row in df.iterrows():
		teams.append([row.tolist()[x] for x in indices_to_use])
	for team in teams[:3]:
		print team
	return teams


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
	folds = StratifiedKFold(Y, 19)
	aucs = []
	for train, test in folds:
		# Sizes
		# print X[train].shape, Y[train].shape
		# print X[test].shape, len(prediction)

		clf.fit(X[train], Y[train])
		prediction_prob = clf.predict_proba(X[test])
		prediction = clf.predict(X[test])
#		print "----Y Test-----"
#		print Y[test]
#		print "====Prediction====="
#		print prediction
		aucs.append(roc_auc_score(Y[test], prediction_prob[:, 1]))
	print clf.__class__.__name__, aucs, numpy.mean(aucs)


def main():
	teams, champs = load()
	X = create_input(teams)
	Y = create_output(teams, champs)

	print X
	print Y

	ps = PredefinedSplit(test_fold=([-1]*532+[0]*30))
	for train_index, test_index in ps:
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = Y[train_index], Y[test_index]
		print "SGD Classifier"
		clf = linear_model.SGDClassifier(loss='log')
		clf.fit(X_train, y_train)
		print clf.predict(X_test)
		print y_test

		print "GaussianNB Classifier"
		clf = GaussianNB()
		clf.fit(X_train, y_train)
		print clf.predict(X_test)
		print y_test

		print "RandomForest Classifier"
		clf = RandomForestClassifier(n_estimators=10, max_depth=10)
		clf.fit(X_train, y_train)
		print clf.predict(X_test)
		print y_test

	clf = linear_model.SGDClassifier(loss='log')
	test_classifier(clf, X, Y)

	clf = GaussianNB()
	test_classifier(clf, X, Y)

	clf = RandomForestClassifier(n_estimators=10, max_depth=10)
	test_classifier(clf, X, Y)


if __name__ == '__main__':
	main()