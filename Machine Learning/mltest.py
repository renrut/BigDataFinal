# conda install scikit-learn
import scipy
import numpy
import csv
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold


# TEAM_ID, TEAM_NAME,GP,W,L,W_PCT,MIN,FGM,FGA,FG_PCT,FG3M,FG3A,FG3_PCT,FTM FTA,FT_PCT,OREB,DREB,REB,AST,TOV,STL,BLK,BLKA,PF,PFD,PTS,PLUS_MINUS,CFID,CFPARAMS

def load_teams():
    with open('/data/season_stats.csv') as fi:
    lines = csv.reader(fi)
    batting = []
    for line in lines:
        if line[0] == '#':
            continue
        batting.append(line.split(','))
    return batting


# playerID,yearID,gameNum,gameID,teamID,lgID,GP,startingPos
def load_allstars():
    with open('/data/game_logs_regular_season.csv') as fi:
    lines = csv.reader(fi)

    all_stars = {}
    for line in lines:
        if line[0] == '#':
            continue
        player = line[0]
        year = line[1]
        all_stars[(player, year)] = 1

    return all_stars


def load():
    return load_batting(), load_allstars()


def create_input(batting):
    # don't want to cinlude playerID, sting, team, league year in predicition
    SKIP = 5
    WIDTH = len(batting[0]) - SKIP
    X = scipy.zeros((len(batting), WIDTH))
    for i in range(0, len(batting)):
        for j in range(SKIP, WIDTH):
                X[i, j-SKIP] = batting[i][j] if batting[i][j] != '' else 0
    return X


def create_output(batting, all_stars):
    Y = scipy.zeros(len(batting))
    for i in range(0, len(batting)):
        player = batting[i][0]
        year = batting[i][1]
        if (player, year) in all_stars:
            Y[i] = 1
    print 'Number of all stars', sum(Y)
    return Y


def test_classifier(clf, X, Y):
    folds = StratifiedKFold(Y, 5)
    aucs = []
    for train, test in folds:
        # Sizes
        # print X[train].shape, Y[train].shape
        # print X[test].shape, len(prediction)

        clf.fit(X[train], Y[train])
        prediction = clf.predict_proba(X[test])
        aucs.append(roc_auc_score(Y[test], prediction[:, 1]))

    print clf.__class__.__name__, aucs, numpy.mean(aucs)

def runClassifier(clf, X, Y):
    folds = StratifiedKFold(Y, 5)
    aucs = []
    for train, test in folds:

        clf.fit(X[train], Y[train])
        prediction = clf.predict_proba(X[test])
        aucs.append(roc_auc_score(Y[test], prediction[:, 1]))


    print clf.__class__.__name__, aucs, numpy.mean(aucs)


def main():
    batting, all_stars = load()
    X = create_input(batting)
    Y = create_output(batting, all_stars)

    # clf = linear_model.SGDClassifier(loss='log')
    # test_classifier(clf, X, Y)

    # clf = GaussianNB()
    # test_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    runClassifier(clf, X, Y)


if __name__ == '__main__':
    main()
