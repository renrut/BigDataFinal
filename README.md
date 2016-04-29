# BigDataFinal
Final project for Vanderbilt Big Data CS3892. 
#Goal
The goal of this project is to accurately predict which NBA teams will make it to the playoffs using data pulled from ESPN.com, Wikipedia, Twitter, and other news sources.

#Model
Our model is a work in progress, but we use player and team popularity, team streakiness, injuries, player records, and playoff history from previous seasons.

#Note
Many of our scripts need to be run in the root folder to properly access the data.

#Dependencies

```
pip install scikit-learn
pip install selenium
Chromedriver - https://sites.google.com/a/chromium.org/chromedriver/
```

#Basketball-Reference Scraper

Scraping Basketball-Reference was a challenge.

ActivePlayerCompiler.py uses selenium web browser automation to open each teams' player roster and totals for a defined year and make a javascript function call to create a csv file for it. Using browser automation proved to be much slower than other types of scraping performed, however it is a lot less suspicious looking. It then takes these files and moves them into a roster directory. 

Note: For it to move rosters and totals into the respective directory, you may need to check out the code towards the bottom of the file. You will also need to update your username and path to the downloads directory if not on a mac or chrome options are changed.

```
python PlayerRosterScraper.py <year>
```
I tried to make it work for every team, however it proved difficult as 

#Stats.NBA Scraper

This was much easier and simply consisted of a few api calls to stats.nba.com
```
python game_log_scraper.py
```

#Map-Reduce
This script makes use of Yelps MRJob module. Therefore it can be deployed on Amazon EMR, a hadoop cluster, or locally with relative ease. Since our data wasn't huge (unfortunately only so much data exists for our application), we chose to run the MRJobs locally. Right now to run each job you need to uncomment it in the main method of playerMR.py

To run the playerMR.py
```
python playerMR.py ../data/allteamsroster.csv > output.txt
python cleaner.py output.txt
```
cleaner.py will take it in as a txt file, and clean it up into comma separated format.

Similarly, to run gamelogMR.py which runs a MapReduce job to see how many games were won thanks to freethrows,

```
python gamelogMR.py ../data/season_stats_regular_season.csv > ftwins.txt
python cleaner.py ftwins.txt
``` 

#Machine Learning
Our machine learning uses scikit-learn on our data. To run it, do
```
python machineLearn.py
```


