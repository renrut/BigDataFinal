import goldsberry as gb
import requests
import pandas as pd
import matplotlib.pyplot as plt
from urllib import urlretrieve
from matplotlib.offsetbox import OffsetImage
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.colors import LinearSegmentedColormap

def draw_court(color='white', lw=2, outer_lines=True):
	# Create the various parts of an NBA basketball court

	# There is a conversion between inches to graph units of 6":5u

	# Create the basketball hoop
	# Diameter of a hoop is 18" so it has a radius of 9", which is a value
	# 7.5 in our coordinate system
	hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

	# Create backboard
	backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

	# The paint
	# Create the outer box 0f the paint, width=16ft, height=19ft
	outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
	# Create the inner box of the paint, widt=12ft, height=19ft
	inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

	# Create free throw top arc
	top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color)
	# Create free throw bottom arc
	bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, 
							color=color, linestyle='dashed')
	# Restricted Zone, it is an arc with 4ft radius from center of the hoop
	restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

	# Three point line
	# Create the side 3pt lines, they are 14ft long before they begin to arc
	corner_three_a = Rectangle((-220, -47.5), 0, 137, linewidth=lw, color=color)
	corner_three_b = Rectangle((220, -47.5), 0, 137, linewidth=lw, color=color)
	# 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
	# I just played around with the theta values until they lined up with the threes
	three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

	# Center Court
	center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
	center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

	# List of the court elements to be plotted onto the axes
	court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
					  bottom_free_throw, restricted, corner_three_a,
					  corner_three_b, three_arc, center_outer_arc,
					  center_inner_arc]

	if outer_lines:
		# Draw the half court line, baseline and side out bound lines
		outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
								color=color, fill=False)
		court_elements.append(outer_lines)

	fig = plt.gcf()

	# Add the court elements onto the axes
	for element in court_elements:
		fig.gca().add_artist(element)

def get_cmap():
	# custom color dict to define the range of colors to represent shot averages relative to league average
	cdict = {'red': ((0,0,0),
					(.25,0,0),
					(.5,1,1),
					(.75,1,1),
					(1,1,1)),
			'green':((0,0,0),
					(.25,.75,.75),
					(.5,1,1),
					(.75,.5,.5),
					(1,0,0)),
			'blue': ((0,1,1),
					(.25,1,1),
					(.5,.75,.75),
					(.75,0,0),
					(1,0,0))}
	# set the cmap to be used to utilize the cdict
	return LinearSegmentedColormap('MyColorDict', cdict)

def get_player_portrait(playerID):
	"""get the player's picture from nba.com"""
	pic = urlretrieve("http://stats.nba.com/media/players/230x185/"+str(playerID)+".png", str(playerID)+".png")
	player_pic = plt.imread(pic[0])
	img = OffsetImage(player_pic, zoom=0.6)
	img.set_offset((600,75))
	plt.gca().add_artist(img)