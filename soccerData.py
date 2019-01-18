# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

country = pd.read_csv('Country.csv')
league = pd.read_csv('League.csv')
match = pd.read_csv('Match.csv')
playeratt = pd.read_csv('Player_Attributes.csv')
player = pd.read_csv('Player.csv')
team = pd.read_csv('Team.csv')
teamatt = pd.read_csv('Team_Attributes.csv')
sqlite = pd.read_csv('sqlite_sequence.csv')

#----------Finding the Most Competitive League------------
#Counting Draw Matches
draw_matches = match[match['home_team_goal'] == match['away_team_goal']]
#Counting Draws in Each League
league_most_draw = np.array([])
for x in league['id']:
    league_most_draw = np.append(league_most_draw,draw_matches[draw_matches['league_id'] == x]['league_id'].count())
#Plotting Draws in Each League
fig1, ax1 = plt.subplots()
ax1.pie(league_most_draw,labels=league['name'])
ax1.axis('equal')
plt.show()

#-------------Top 5 Teams with Most Goals per Game-------------
team_goals = np.zeros((1,3))          #Column [0,1,2] = [home,away,total]
for x in team['team_api_id']:
    home_goals_temp = match[match['home_team_api_id'] == x]['home_team_goal'].sum()
    away_goals_temp = match[match['away_team_api_id'] == x]['away_team_goal'].sum()
    total_goals_temp = home_goals_temp + away_goals_temp
    temp = [home_goals_temp, away_goals_temp, total_goals_temp]
    team_goals = np.vstack([team_goals,np.array(temp)])

team_goals = team_goals[1:, :]


   