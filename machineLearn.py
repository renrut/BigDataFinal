import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold


# SEASON_ID,TEAM_ID,TEAM_NAME,GP,W,L,W_PCT,MIN,FGM,FGA,FG_PCT,FG3M,FG3A,FG3_PCT,FTM,FTA,FT_PCT,OREB,DREB,REB,AST,TOV,STL,BLK,BLKA,PF,PTS,PLUS_MINUS
def load_teams():
	f = open('data/season_stats_regular_season.csv', 'r')
	df = pd.read_csv('data/season_stats_regular_season.csv')
	lines = f.readlines()
	f.close()

	teams = []
	for line in lines[1:]:
		line = line.strip()
		if line[0] == '#':
			continue
		teams.append(line.split(','))
	print "---------------TEAMS--------------"
	print teams
	return teams


# TEAM_ID, SEASON_ID, champs
def load_champs():
	f = open('data/champs.csv', 'r')
	lines = f.readlines()
	f.close()

	champs = {}
	for line in lines:
		line = line.strip().split(',')
		if line[0] == '#':
			continue
		team = line[0]
		year = line[1]
		if line[2]==1.0:
			champs[(team, year)] = 1
		else:
			champs[(team, year)] = 0
	print "------------------CHAMPS------------------"
	print champs
	return champs


def load():
	return load_teams(), load_champs()


def create_input(teams):
	# don't want to cinlude playerID, sting, team, league year in predicition
	SKIP = 6
	WIDTH = len(teams[0]) - SKIP
	X = scipy.zeros((len(teams), WIDTH))
	for i in range(0, len(teams)-30):
		for j in range(SKIP, WIDTH):
				X[i, j-SKIP] = teams[i][j] if teams[i][j] != '' else 0
	print "---------X--------------"
	print X
	return X


def create_output(teams, champs):
	Y = scipy.zeros(len(teams))
	for i in range(0, len(teams)):
		player = teams[i][0]
		year = teams[i][1]
		if (player, year) in champs:
			Y[i] = 1
	print 'Number of champs', sum(Y)
	print "---------Y--------------"
	print Y
	return Y


def test_classifier(clf, X, Y):
	folds = StratifiedKFold(Y, 19)
	aucs = []
	for train, test in folds:
		# Sizes
		# print X[train].shape, Y[train].shape
		# print X[test].shape, len(prediction)

		clf.fit(X[train], Y[train])
		prediction = clf.predict_proba(X[test])
		aucs.append(roc_auc_score(Y[test], prediction[:, 1]))
	print clf.__class__.__name__, aucs, numpy.mean(aucs)


def main():
	teams, champs = load()
	X = create_input(teams)
	Y = create_output(teams, champs)

	clf = linear_model.SGDClassifier(loss='log')
	test_classifier(clf, X, Y)

	clf = GaussianNB()
	test_classifier(clf, X, Y)

	clf = RandomForestClassifier(n_estimators=10, max_depth=10)
	test_classifier(clf, X, Y)


if __name__ == '__main__':
	main()