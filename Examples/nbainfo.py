'''
NBA Teams Roster
https://en.wikipedia.org/wiki/List_of_current_NBA_team_rosters
'''

teams_list = ['Boston Celtics','New Jersey Nets',
'New York Knicks','Philadelphia 76ers','Toronto Raptors',
'Chicago Bulls','Cleveland Cavaliers','Detroit Pistons',
'Indiana Pacers','Milwaukee Bucks','Atlanta Hawks','Charlotte Bobcats',
'Miami Heat','Orlando Magic','Washington Wizards','Denver Nuggets',
'Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers',
'Utah Jazz','Golden State Warriors','Los Angeles Clippers','Los Angeles Lakers',
'Phoenix Suns','Sacramento Kings','Dallas Mavericks','Houston Rockets','Memphis Grizzlies',
'New Orleans Hornets','San Antonio Spurs']


class Player():
	name = ""
	#avg points per game
	ppg = 0
	popularity = .0
	injured = False

	def __init__(self, name, ppg, popularity, injured):
		self.name = name
		self.ppg = ppg
		self.popularity = popularity
		self.injured = injured


class Team():
	#list of player objects
	players = []
	#current streak
	streak = 0

	#pastPlayoffs is a decimal from past 5 years
	#1.0 would mean the team has been in the past 5
	#NBA playoffs
	pastPlayoffs = .0
	wins = 0
	losses = 0
	popularity = .0

	def __init__(self, name, players, streak,pastPlayoffs,wins,losses,popularity):
		self.players = players
		self.streak = streak
		self.pastPlayoffs = pastPlayoffs
		self.wins = wins
		self.losses = losses
		self.popularity = popularity


def calculatedPopularity(name):
	''' This method will take a string that could either
	be a team name or a player name and query twitter and
	other news sources to 