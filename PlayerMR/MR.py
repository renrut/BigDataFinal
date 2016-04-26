
from mrjob.job import MRJob
from mr3px.csvprotocol import CsvProtocol
import sys
import os
import csv

'''
Count the number of tweets. 
Parse tweets with json.loads -- note how the tweets are huge JSON blobs.
Ignore tweets that error on load.
'''

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




class Colleges(MRJob):

    def mapper(self, _, line):
        try:
            #line.split(',')
            yield "player", 1
        except:
            pass
        
    def reducer(self, _, counts):
        yield 'players', sum(counts)


    
if __name__ == '__main__':
    PlayerWeight.run()