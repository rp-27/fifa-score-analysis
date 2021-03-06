## FIFA Score Analysis and Modeling Project

This project is about using the rich scoring data provided by EA's FIFA team to see if there are certain characteristics or skills that set top football players apart from the rest and if there any patterns that can help us predict the next generation of star players.

## Files and Usage

The code and data used for the project can be split into two categoies: 1. the scripts used for data collection and cleaning, and 2. the data and dependencies for the project's Jupyter Notebook environment, which can be launched via the Binder badge found at the bottom of the page.

### Project Files:

FIFA scoring data can be downloaded using the following link: https://www.kaggle.com/stefanoleone992/fifa-20-complete-player-dataset

1. values_scraper.py: Web scraper built to get values of the top 500 players on Transfermarkt.us. Writes a 'final_url_list.csv' file (list of player urls at time of scraping for reference if needed) and a 'values_2.csv' file (data of top current players and their yearly mean values from 2014-2019)
1. long_names_scraper.py: Web scraper to get long name values of players from Transfermarkt.us in order to merge the disparate name fields, which will allow us to merge the FIFA and Transfermarkt.us data. Writes a 'name_fields.csv' file (with the common name and long name of players)
1. merge_values_fifa_on_name.py: Script to merge the the FIFA and Transfermarkt.us data, using the 'values_2.csv' and 'name_fields.csv' files. Rename path from lines 6-11 with local path to FIFA data to run. Results in 'merged_fifa_[year].csv' tables and includes code at bottom to find players in the FIFA 2020 dataset that are not in the current top 500 ('new_players_20.csv'), which is used in analysis in the Jupyter Notebook
1. team_name_scraper.py: Web scraper to get team names and associated ids from Sofifa. This is in order to merge teams with leagues (from the 'teams_and_leagues.csv' file downloaded with the FIFA data) which is used for analysis in the Jupyter Notebook

### Jupyter Notebook Files:

1. FIFA Score Analysis.ipynb: File for the Jupyter Notebook with analysis and modeling for the given data
1. project data (folder): Contains all the data necessary for the Jupyter notebook enviroment and an example of the final data generated by the scripts mentioned above. 

## Project Analysis and Write-Up

The write-up for the project can be found here: https://rp-27.github.io/posts/predicting-the-next-football-superstar/

Jupyter Notebook:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/rp-27/fifa-score-analysis/main?filepath=FIFA%20Score%20Analysis.ipynb)
