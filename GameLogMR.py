from mrjob.job import MRJob
import sys
import os

# BLANK ROW
# SEASON_ID
# TEAM_ID
# TEAM_ABBREVIATION
# TEAM_NAME
# GAME_ID
# GAME_DATE
# MATCHUP
# WL
# MIN
# FGM
# FGA
# FG_PCT
# FG3M
# FG3A
# FG3_PCT
# FTM
# FTA
# FT_PCT
# OREB
# DREB
# REB
# AST
# STL
# BLK
# TOV
# PF
# PTS
# PLUS_MINUS
# VIDEO_AVAILABLE

#gets number of wins for each team over the season
class GameCount(MRJob):

    def mapper(self, _, line):
        try:
            data = line.split(',')
            seasonid = data[1]
            teamid = data[2]
            wl = data[8]
            if wl is 'W':
                wl = 1
            else:
                wl = 0

            yield (seasonid, teamid), wl
        except:
            pass
        
    def reducer(self, team, wins):
        wins = sum(wins)
        if wins != 0:
            yield team, wins

if __name__ == '__main__':
    GameCount.run()
