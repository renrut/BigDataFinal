# BigDataFinal
Final project for Vanderbilt Big Data CS3892. 
#Goal
The goal of this project is to accurately predict which NBA teams will make it to the playoffs using data pulled from ESPN.com, Wikipedia, Twitter, and other news sources.

#Model
Our model is a work in progress, but we use player and team popularity, team streakiness, injuries, player records, and playoff history from previous seasons.

#Dependencies

pip install scikit-learn

pip install selenium

#Basketball-Reference Scraper

Scraping Basketball-Reference was a challenge.

ActivePlayerCompiler.py uses selenium web browser automation to open each teams' player roster and totals for a defined year and make a javascript function call to create a csv file for it. Using browser automation proved to be much slower than other types of scraping performed, however it is a lot less suspicious looking. It then takes these files and moves them into a roster directory.