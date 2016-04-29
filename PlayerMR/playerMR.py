
from mrjob.job import MRJob
import sys
import os
import champions


#gets average player weight for each team
class PlayerWeight(MRJob):
    # OUTPUT_PROTOCOL = CsvProtocol
    # INPUT_PROTOCOL = CsvProtocol

    def mapper(self, _, line):
        try:
            data = line.split(',')
            weight = data[4]
            team = data[8]
            year = data[9]
            yield (team, year), int(weight)
        except:
            pass
        
    def reducer(self, team, weight):
        weight = list(weight)
        avgweight = (sum(weight))/(len(weight))
        yield team, avgweight



#counts winning colleges
class Colleges(MRJob):

    def mapper(self, _, line):
        try:
            data = line.split(',')
            college = data[7]
            team = data[8]
            year = int(data[9])
            win = champions.isChamp(team, year)
            yield college, win
        except:
            pass
        
    def reducer(self, college, win):
        wincount = sum(win)
        if wincount>0:
            yield college, wincount

#0 31
#1 Mike Muscala
#2 PF
#3 11-Jun
#4 240
#5 July 1 1991
#6 R
#7 Bucknell University
#8 ATL
#9 2014
#POS, WEIGHT, AGE, WIN
class TeamAvg(MRJob):
    "[win,pos] [avg. age, avg. weight]"
    def mapper(self, _, line):
        data = line.split(',')
        pos = data[2]
        year = int(data[9])
        age = year - int(data[5][-4:])
        weight = int(data[4])
        team = data[8]
        win = champions.isChamp(team, year)
        yield (win,pos), (age, weight)


    def reducer(self, win, player):
        player = list(player)
        tot = sum([p[0] for p in player])
        ageavg = tot/len(player)
        weightavg = sum([p[1] for p in player])/len(player)
        yield win, (ageavg, weightavg)

#MR Job gets the average number of player seasons for team
class SeasonCount(MRJob):
    "[win,pos] [avg. age, avg. weight]"
    def mapper(self, _, line):
        data = line.split(',')
        year = int(data[9])
        seasons = data[6]
        if seasons is "R":
            seasons = 0
        seasons = int(seasons)
        team = data[8]
        win = champions.isChamp(team, year)
        yield (win, team, year), seasons


    def reducer(self, win, seasons):
        seasons = list(seasons)
        seasonsavg = sum(seasons)/len(seasons)
        yield win, seasonsavg


#MR Job gets the average number of player seasons for team
class PlayerPER(MRJob):
    def mapper(self, _, line):
        #split data lines into list
        data = line.split(',')
        team = data[8]#MAY NEED TO CHANGE
        year = int(data[9])
        playerPER = 0#make functioncall here
        yield (year, team), playerPER

    def reducer(self, team, playerPER):
        #may need to typecast generator to list, but dont think so...
        yield team, sum(playerPER)


#output should be avg weight for PG, C, PF, SF, SG on winning teams
    
if __name__ == '__main__':
    #SeasonCount.run()
    #TeamAvg.run()
    #Colleges.run()
    PlayerPER.run()
