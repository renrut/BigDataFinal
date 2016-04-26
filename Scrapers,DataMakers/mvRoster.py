import os

move = os.getcwd()+"/data/PlayerRosters/"
for i in os.listdir(name):
    if "roster" in i: 
        os.rename(name + i, move + i)
    else:
        continue