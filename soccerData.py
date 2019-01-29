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


#---------------User Defined Functions----------------
def drawMatches(dataset):               # Function to find drawn matches from dataset
    data = match[match['home_team_goal'] == match['away_team_goal']]
    return data

def removeNull(dataset):                #Function to remove Null Columns
    data = dataset.dropna(how='any',axis=1)
    return data

def league_count(x):                    #Function to count league occurences in drawn matches
    count = np.array([])
    count = np.append(count,draw_matches[draw_matches['league_id'] == x]['league_id'].count())
    return count

def goals_matches(x):                   #Function to count total,home,away goals and total matches 
    home_goals_temp = match[match['home_team_api_id'] == x]['home_team_goal'].sum()
    away_goals_temp = match[match['away_team_api_id'] == x]['away_team_goal'].sum()
    total_goals_temp = home_goals_temp + away_goals_temp
    total_matches_team = home_matches_count[x] + away_matches_count[x]
    return total_goals_temp,home_goals_temp,away_goals_temp,total_matches_team

def tupleToNumpy(var):                  #Function to convert tuple into Numpy Array
    var = np.array(var)
    var.flatten();
    return var

#-------Finding Correlation Matrix----------------
plt.matshow(match.corr())


'''Last columns of 'match' table are highly coorelated so its better to remove 
them for my particular analysis'''

#------------Data Wrangling---------

    #Removing Null Values
match = removeNull(match)
team = removeNull(team)
teamatt = removeNull(teamatt)

    #Removing Columns   
match = match.drop(['id','country_id'],axis=1) # 'country_id' is redundant  & 'id' is not used
league = league.drop(['id'],axis=1)            # 'id' is redundant



#----------Finding the Most Competitive League------------
#Counting Draw Matches
draw_matches = drawMatches(match)
#Counting Draws in Each League
league_most_draw = np.array([])

league_most_draw = league['country_id'].apply(league_count) #Used Apply function in place of for loop 

#Plotting Pie Chart for Draws in Each League
fig1, ax1 = plt.subplots()
ax1.pie(league_most_draw,labels=league['name'])
ax1.axis('equal')
plt.show()


#-------------Most Attacking Team-------------

home_matches_count = match['home_team_api_id'].value_counts()       
away_matches_count = match['away_team_api_id'].value_counts()

#Used Apply function in place of for loop
team_goals,home_goals,away_goals,total_matches_team = zip(*team['team_api_id'].apply(goals_matches))    

home_goals = tupleToNumpy(home_goals)
away_goals = tupleToNumpy(away_goals)
team_goals = tupleToNumpy(team_goals)


average_goals = team_goals / total_matches_team     #Averaging Goals by each team
temp = np.sort(average_goals)
most_goals_per_game = temp[::-1]
most_goals_per_game = most_goals_per_game[0:5]
most_goals_per_game_team = []

for y in most_goals_per_game:
    for i,val in enumerate(average_goals):
        if val == y:
            most_goals_per_game_team.append(team['team_long_name'][i])
            break
        
#Bar Chart for Average Goals
index = np.arange(5)
plt.bar(index,most_goals_per_game,color='b',align='center',width=0.2)
plt.xticks(index,most_goals_per_game_team)
plt.xlabel('Teams')
plt.ylabel('No of Goals Scored per Game')
plt.title('Most Attacking Teams According to Goals Scored per Game')
plt.show()


#----------------Where are Teams Most Likely to Score? Home & Away Goals Pattern of Top 5 Scoring Teams----------------

temp2 = np.sort(team_goals)
most_goals_overall =  temp2[::-1]           #Reversing the Array
most_goals_overall = most_goals_overall[0:5]
most_goals_overall_home = np.array([])
most_goals_overall_away = np.array([])
most_goals_overall_team = []
for z in most_goals_overall:
    for i,val in enumerate(team_goals):
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

