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
#Plotting Pie Chart for Draws in Each League
fig1, ax1 = plt.subplots()
ax1.pie(league_most_draw,labels=league['name'])
ax1.axis('equal')
plt.show()

#-------------Most Attacking Team-------------
team_goals = np.zeros((1,3))          #Column [0,1,2] = [home,away,total]
total_matches_team = np.array([])     #Tota Matches played by Each Team
home_matches_count = match['home_team_api_id'].value_counts()       
away_matches_count = match['away_team_api_id'].value_counts()

for x in team['team_api_id']:
    home_goals_temp = match[match['home_team_api_id'] == x]['home_team_goal'].sum()
    away_goals_temp = match[match['away_team_api_id'] == x]['away_team_goal'].sum()
    total_goals_temp = home_goals_temp + away_goals_temp
    temp = [home_goals_temp, away_goals_temp, total_goals_temp]
    team_goals = np.vstack([team_goals,np.array(temp)])
    total_matches_team = np.append(total_matches_team,home_matches_count[x] + away_matches_count[x])

team_goals = team_goals[1:, :]
home_goals = team_goals[:,0]
away_goals = team_goals[:,1]
average_goals = team_goals[:,2] / total_matches_team     #Averaging Goals by each team
temp = np.sort(average_goals)
most_goals_per_game = temp[::-1]
most_goals_per_game = most_goals_per_game[0:5]
most_goals_per_game_team = []
for y in most_goals_per_game:
    for i,val in enumerate(average_goals):
        if val == y:
            most_goals_per_game_team.append(team['team_long_name'][i])
            break
#Bar Chart for AVerage Goals
index = np.arange(5)
plt.bar(index,most_goals_per_game,color='b',align='center',width=0.2)
plt.xticks(index,most_goals_per_game_team)
plt.xlabel('Teams')
plt.ylabel('No of Goals Scored per Game')
plt.title('Most Attacking Teams According to Goals Scored per Game')
plt.show()

#----------------Where are Teams Most Likely to Score? Home & Away Goals Pattern of Top 5 Scoring Teams----------------
temp2 = np.sort(team_goals[:,2])
most_goals_overall =  temp2[::-1]           #Reversing the Array
most_goals_overall = most_goals_overall[0:5]
most_goals_overall_home = np.array([])
most_goals_overall_away = np.array([])
most_goals_overall_team = []
for z in most_goals_overall:
    for i,val in enumerate(team_goals[:,2]):
        if val == z:
            most_goals_overall_team.append(team['team_long_name'][i])
            most_goals_overall_home = np.append(most_goals_overall_home,home_goals[i])
            most_goals_overall_away = np.append(most_goals_overall_away,away_goals[i])       
            break

#Stacked Bar Chart for Home and Away Goals 
index = np.arange(5)
p1 = plt.bar(index,most_goals_overall_home,color='g',align='center',width=0.3,yerr=index)
p2 = plt.bar(index,most_goals_overall_away,color='r',align='center',width=0.3,yerr=index,bottom=most_goals_overall_home)
plt.xticks(index,most_goals_overall_team)
plt.xlabel('Teams')
plt.ylabel('No of Goals Scored ( Home vs Away)')
plt.title('Home vs Away Goals of Most Scored Teams')
plt.legend((p1[0],p2[0]),('Home','Away'))
plt.show()