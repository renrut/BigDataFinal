from mrjob.job import MRJob
import sys
import os

#0 SEASON_ID
#1 TEAM_ID
#2 TEAM_ABBREVIATION
#3 TEAM_NAME
#4 GAME_ID
#5 GAME_DATE
#6 MATCHUP
#7 WINS LOSS
#8 MINUTES
#9 FIELD GOAL MADE
#10 FIELD GOAL ATTMEPT
#11 FG_PCT
#12 FG3 PTR MADE
#13 FG3 PTR ATTEMPT
#14 FG 3 PTR _ PERCENT
#15 FREE THROWS MADE
#16 FREE THROWS ATTEMPTED
#17 FT_PCT
#18 OFF. REBOUND
#19 DEF. REBOUND
#20 REBOUND
#21 ASSIST
#22 STEAL
#23 BLOCK
#24 TURNOVER
#25 PERSONAL FOULS
#26 PTS
#27 PLUS_MINUS
#28 VIDEO_AVAILABLE

#sees how freethrow dependent teams are
class FTWins(MRJob):
    #map by game id

    def mapper(self, _, line):
        try:
            data = line.split(',')
            gameid = int(data[4])
            pts = int(data[26])
            ftpts = int(data[15])
            teamid = data[1]
            seasonid = int(data[0])-40000
            wl = int(data[7])
            yield gameid, (wl, teamid, seasonid, pts, ftpts)
        except:
            pass
        
    def combiner(self, _, ftdata):
        #ftdata will be of length 2 (2 teams per game).
        #if not, data is incomplete and it will be ignored
        ftdata = list(ftdata)
        if len(ftdata) is 2:
            winningindex = 0
            losingindex = 1
            #changes index of winning team
            if ftdata[0][0] is 0:
                winningindex = 1
                losingindex = 0
            #get team and season of winning team
            team = ftdata[winningindex][1]
            season = ftdata[winningindex][2]
            #get number of points team won by
            ptdiff = ftdata[winningindex][3] - ftdata[losingindex][3]
            # number of freethrows made
            ftmade = ftdata[winningindex][4]
            #Checks if winning team would have won without freethrows
            if ftmade > ptdiff:
                ftdependent = 1
            else:
                ftdependent = 0
                
            yield (season, team), ftdependent
    
    def reducer(self, key, ftdep):
        yield (key[0], int(key[1])), sum(ftdep)



#gets number of wins for each team over the season
class GameCount(MRJob):

    def mapper(self, _, line):
        try:
            data = line.split(',')
            seasonid = data[0]
            teamid = data[1]
            wl = data[7]

            yield (seasonid, teamid), 1
        except:
            pass
        
    def reducer(self, team, wins):
        wins = sum(wins)
        if wins != 0:
            yield team, wins



if __name__ == '__main__':
    FTWins.run()
