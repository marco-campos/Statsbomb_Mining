
import matplotlib.pyplot as plt
from pandas import json_normalize
import numpy as np
import json
from FCPython import createPitch

pitchLengthX = 120
pitchWidthY= 80

match_id_required = 3795506

file_name= str(match_id_required)+'.json'

with open('Statsbomb/data/events/' + file_name) as data_file:
    data=json.load(data_file)
    
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])
    

def pitchPasses():
    #A dataframe of shots
    
    passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
        
#Draw the pitch
    (fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
    for i,thepass in passes.iterrows():
    #if thepass['team_name']==away_team_required: #
        if thepass['player_name']=='Lorenzo Insigne':
            x=thepass['location'][0]
            y=thepass['location'][1]
            passCircle=plt.Circle((x,pitchWidthY-y),1.5,color="blue")      
            passCircle.set_alpha(.2)   
            ax.add_patch(passCircle)
            dx=thepass['pass_end_location'][0]-x
            dy=thepass['pass_end_location'][1]-y

            passArrow=plt.Arrow(x,pitchWidthY-y,dx,-dy,width=1,color="blue")
            ax.add_patch(passArrow)

    fig.set_size_inches(10, 7)
    fig.savefig('Output/passes.pdf', dpi=100) 
    plt.show()
    
def showLineups():
    teams = df.loc[df['type_name']=='Starting XI'].set_index('id')
    
    #Draw the pitch
    (fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
    
    for i,team in teams.iterrows():
        if (team['index'] ==1):
            pitch = 'left'
        elif (team['index'] ==2):
            pitch = 'right'
        print(pitch)
        print("Team: " + team['team_name'] + "\nFormation: " + str(int(team['tactics_formation'])))
        lineup_data=team['tactics_lineup']
        for player in lineup_data:
            print(player['player']['name'])
            position =player['position']['name']
            print(position + '\n')
            if (position == 'Goalkeeper'):
                x = 5
                y = pitchWidthY/2
                passCircle=plt.Circle((x,y),1.5,color="blue")
                passCircle.set_alpha(.2)
                ax.add_patch(passCircle)
                plt.text((x+1),y+1,player['player']['name'])
        fig.set_size_inches(10, 7)
        fig.savefig('Output/euro2020GK.pdf', dpi=100) 
        plt.show()
            
def showClearances():

    clearances = df.loc[df['type_name'] =='Clearance'].set_index('id')
    (fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
    index = 1
    clearance_data = {}
    for i,clearance in clearances.iterrows():
    #if thepass['team_name']==away_team_required: #
        
        clearedBy= clearance['player_name']
        print('Clearance: ' + str(index) +  " by " + clearance['player_name'])
        index +=1
        if (clearedBy in clearance_data):
            clearance_data[clearedBy] += 1
        else:
            clearance_data[clearedBy] =1
        print(clearance_data)
    most_clearances = max(clearance_data, key=clearance_data.get)
    print(most_clearances)

    fig.set_size_inches(10, 7)
    fig.savefig('Output/passes.pdf', dpi=100) 
    plt.show()

def playerPosition(team, row, column, pitchLengthX, pitchWidthY):
    dx = pitchLengthX/12
    offsetX = pitchLengthX/24
    dy = pitchWidthY/5
    offsetY = pitchWidthY /10
    if (team == 'home'):
        x = dx * (column-1) + offsetX
        y = dy * (row-1) + offsetY
    elif (team =='away'):
        x = dx * (12 - column + 1) - offsetX
        y = dy * (5- row+1) - offsetY
    else: 
        x = 10
        y= 10
    return [x,y]
    
def mapPosition(team, position, pitchLengthX, pitchWidthY):
    positions ={
        "Goalkeeper": playerPosition(team, 3, 1, pitchLengthX, pitchWidthY),
        "Left Back": playerPosition(team, 5, 2, pitchLengthX, pitchWidthY),
        "Left Center Back": playerPosition(team, 4, 2, pitchLengthX, pitchWidthY),
        "Center Back": playerPosition(team,3, 2, pitchLengthX, pitchWidthY),
        "Right Center Back": playerPosition(team,2, 2, pitchLengthX, pitchWidthY),
        "Right Back": playerPosition(team,1, 2, pitchLengthX, pitchWidthY),
        "Left Wing Back": playerPosition(team,5, 3, pitchLengthX, pitchWidthY),
        "Left Defensive Midfield": playerPosition(team,4, 3, pitchLengthX, pitchWidthY),
        "Center Defensive Midfield": playerPosition(team,3, 3, pitchLengthX, pitchWidthY),
        "Right Defensive Midfield": playerPosition(team,2, 3, pitchLengthX, pitchWidthY),
        "Right Wing Back": playerPosition(team,1, 3, pitchLengthX, pitchWidthY),
        "Left Center Midfield": playerPosition(team,4, 4, pitchLengthX, pitchWidthY),
        "Center Midfield": playerPosition(team,3, 4, pitchLengthX, pitchWidthY),
        "Right Center Midfield": playerPosition(team,2, 4, pitchLengthX, pitchWidthY),
        "Left Midfield": playerPosition(team,5, 5, pitchLengthX, pitchWidthY),
        "Left Attacking Midfield": playerPosition(team,4, 5, pitchLengthX, pitchWidthY),
        "Center Attacking Mifield": playerPosition(team,3, 5, pitchLengthX, pitchWidthY),
        "Right Attacking Midfield": playerPosition(team,2, 5, pitchLengthX, pitchWidthY),
        "Right Midfield": playerPosition(team,1, 5, pitchLengthX, pitchWidthY),
        "Left Wing": playerPosition(team,5, 6, pitchLengthX, pitchWidthY),
        "Center Forward": playerPosition(team,3, 6, pitchLengthX, pitchWidthY),
        "Right Wing": playerPosition(team,1, 6, pitchLengthX, pitchWidthY),
        }
    return positions[position]
    
    

def showFormations():
    teams = df.loc[df['type_name']=='Starting XI'].set_index('id')

    (fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
    
    for i,team in teams.iterrows():
        if (team['index'] ==1):
            teamside = 'home'
        elif (team['index'] ==2):
            teamside = 'away'
        print(teamside)
        print("Team: " + team['team_name'] + "\nFormation: " + str(int(team['tactics_formation'])))
        lineup_data=team['tactics_lineup']
        for player in lineup_data:
            player_name= player['player']['name']
            player_position =player['position']['name']
            print(player_position)
            [x,y] = mapPosition(teamside, player_position, pitchLengthX, pitchWidthY)
            passCircle=plt.Circle((x,y),1.5,color="blue")
            passCircle.set_alpha(.2)
            ax.add_patch(passCircle)
            [x_name_offset, y_name_offset] = [0,3]
            if (teamside == "home" and (player_position =="Center Forward" or player_position == "Left Wing" or player_position =="Right Wing")):
               if (player_position == "Goalkeeper"):
                   y_name_offset+=2
               x_name_offset = -10
            elif (teamside == "away" and (player_position !="Center Forward" and player_position != "Left Wing" and player_position !="Right Wing")):
                x_name_offset = -8
            
            plt.text((x+x_name_offset),y+y_name_offset, player_name)
    fig.set_size_inches(15, 10.5)
    fig.savefig('Output/euro2020_final_lineups.pdf', dpi=100) 
    plt.show()
    
    
    fig.set_size_inches(10, 7)
    fig.savefig('Output/euro2020GK.pdf', dpi=100) 
    plt.show()
    
showFormations()
    
    