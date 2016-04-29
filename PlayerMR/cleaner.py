from __future__ import print_function
import sys


#Cleans up MR output into a csv format

name = sys.argv[1]
newname = sys.argv[1].replace(".txt", ".csv")
f = open(sys.argv[1], "r")
fi = open(sys.argv[1]+".csv" , "wb")
for row in f:
	row = row.replace("[","")
	row = row.replace("]","")
	row = row.replace("\t",", ")
	print(row, file=fi)

fi.close()
f.close()