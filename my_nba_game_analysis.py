import pandas as pd 
import re

url='https://storage.googleapis.com/qwasar-public/nba_game_warriors_thunder_20181016.txt'

colunm_name=['PERIOD', 'REMAINING_SEC','RELEVANT_TEAM','AWAY_TEAM','HOME_TEAM','AWAY_SCORE','HOME_SCORE','DESCRIPTION']

#Importing data 
plays_data=pd.read_csv(url,delimiter='|',names=colunm_name)

# print(plays_data)

#Extracting all the players name from the dataset
def find_all_players(plays_data):
    list_players=[]

    for i in range(len(plays_data)):
        name=re.search(r"\w\. \w+",plays_data["DESCRIPTION"][i])
        if name:
            name=name.group(0)
            if name not in list_players:
                list_players.append(name)
    return list_players

#Extracting each player statictics
def find_stats_for_each_player(plays_data):
    list_players=find_all_players(plays_data)
    # print(list_players)
    list_stats=[]

    for player in list_players:
        player_data={"player_name":'',"FG":0,"FGA":0,"FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
        player_data['player_name']=player

        for i in range(len(plays_data)):
            name=re.search(r'\w\. \w+',plays_data["DESCRIPTION"][i])
            two_pt=re.search(r"(\w\. \w+) makes 2-pt",plays_data["DESCRIPTION"][i])
            two_pt_at=re.search(r"(\w\. \w+) misses 2-pt",plays_data["DESCRIPTION"][i])
            three_pt=re.search(r"(\w\. \w+) makes 3-pt",plays_data["DESCRIPTION"][i])
            three_pt_at=re.search(r"(\w\. \w+) misses 3-pt",plays_data["DESCRIPTION"][i])
            free_throw=re.search(r"(\w\. \w+) makes free throw",plays_data["DESCRIPTION"][i])
            free_throw_clear=re.search(r"(\w\. \w+) makes clear path free throw",plays_data["DESCRIPTION"][i])
            free_throw_at=re.search(r"(\w\. \w+) misses free throw",plays_data["DESCRIPTION"][i])
            free_throw_clear_at=re.search(r"(\w\. \w+) misses clear path free throw",plays_data["DESCRIPTION"][i])
            def_reb=re.search(r"Defensive rebound by (\w\. \w+)",plays_data["DESCRIPTION"][i])
            off_reb=re.search(r"Offensive rebound by (\w\. \w+)",plays_data["DESCRIPTION"][i])
            assists=re.search(r"(assist by) (\w\. \w+)",plays_data["DESCRIPTION"][i])
            turnover=re.search(r'Turnover by (\w\. \w+)',plays_data["DESCRIPTION"][i])
            steal=re.search(r'(steal by) (\w\. \w+)',plays_data["DESCRIPTION"][i])
            block=re.search(r'(block by) (\w\. \w+)',plays_data["DESCRIPTION"][i])
            foul=re.search(r'foul by (\w\. \w+)',plays_data["DESCRIPTION"][i])

            if name:
                name_temp=name.group(0)
                if name_temp==player:
                    if two_pt:
                        player_data['FG'] +=1
                        player_data['FGA'] +=1
                    if two_pt_at:
                        player_data['FGA'] +=1
                    if three_pt:
                        player_data['3P'] +=1
                        player_data['3PA'] +=1
                        player_data['FG'] +=1
                        player_data['FGA'] +=1
                    if three_pt_at:
                        player_data['3PA'] +=1
                        player_data['FGA'] +=1
                    if free_throw or free_throw_clear:
                        player_data['FT'] +=1
                        player_data['FTA'] +=1
                    if free_throw_at or free_throw_clear_at:
                        player_data['FTA'] +=1
                    if def_reb:
                        player_data['DRB'] +=1
                        player_data['TRB'] +=1
                    if off_reb:
                        player_data['ORB'] +=1
                        player_data['TRB'] +=1
                    if foul:
                        player_data["PF"] +=1
                    if turnover:
                        player_data['TOV'] +=1
                
                if assists:
                    name_ast=assists.group(2)
                    if name_ast == player:
                        player_data["AST"] +=1
                if steal:
                    name_stl=steal.group(2)
                    if name_stl == player:
                        player_data['STL']
                if block:
                    name_blk=block.group(2)
                    if name_blk == player:
                        player_data['BLK'] +=1

#Let's calculate total pts and %
                if player_data['FG'] !=0:
                    player_data['PTS'] =2*(player_data['FG']-player_data["3P"])+3*(player_data["3P"])+player_data["FT"]
                else:
                    player_data['PTS'] =0

                if player_data['FGA'] !=0:
                    player_data['FG%'] = round((player_data['FG']/player_data['FGA']),3)
                else:
                    player_data['FG%'] = 0
                
                if player_data["3PA"] != 0:
                    player_data["3P%"] = round((player_data["3P"]/player_data["3PA"]),3)
                else:
                    player_data["3P%"] = 0

                if player_data["FTA"] !=0:
                    player_data['FT%'] =round((player_data["FT"]/player_data["FTA"]),3)
                else:
                    player_data['FT%'] =0
        list_stats.append(player_data)
    return list_stats

list_stats=find_stats_for_each_player(plays_data)
# print(list_stats)

#This function take the play by play data and the list of each players statistique and return a
#Separated list of each team (list of away team players and list of home team players)
def separate_away_and_home_team(plays_data,list_stats):
    list_away_team=[]
    list_home_team=[]
    # print(len(list_stats))
    for i in range(len(list_stats)):
        current_player=list_stats[i]["player_name"]

        for j in range(len(plays_data)):
            name = re.search(r'(\w\. \w+)',plays_data["DESCRIPTION"][j])
            foul=re.search(r'foul by \w\. \w+', plays_data["DESCRIPTION"][j])
            if name:
                name_temp=name.group()
                if current_player == name_temp and plays_data['RELEVANT_TEAM'][j]==plays_data["HOME_TEAM"][j]:
                    if (list_stats[i] not in list_home_team) and foul==None:
                        list_home_team.append(list_stats[i])
                elif current_player == name_temp and plays_data['RELEVANT_TEAM'][j]==plays_data["AWAY_TEAM"][j]:
                    if (list_stats[i] not in list_away_team) and foul==None:
                        list_away_team.append(list_stats[i])
    return list_home_team ,list_away_team

# home_team=separate_away_and_home_team(plays_data,list_stats)[0]
# print(home_team)

# PART I ANALYSING AND GAME
def analyse_nba_game(play_by_play_moves):
    list_stats=find_stats_for_each_player(plays_data)
    home_team=separate_away_and_home_team(plays_data,list_stats)[0]
    away_team=separate_away_and_home_team(plays_data,list_stats)[1]
    return {"home_team": {"name": play_by_play_moves["HOME_TEAM"][0], "players_data": home_team}, "away_team": {"name": play_by_play_moves["AWAY_TEAM"][0], "players_data": away_team}}

team_dict=analyse_nba_game(plays_data)
print(team_dict)
#PART 2 PRINTING 
def print_nba_game_stats(team_dict):
    headers =[keys for keys in team_dict[0].keys()]
    print(*headers,sep="\t")

    for i in range(len(team_dict)):
        print(*team_dict[i].values(),sep="\t")

    stat_total={"Team Totals":"Team Totals","FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
    
    #print totals
    for i in range(len(team_dict)):
        stat_total['FG'] += team_dict[i]["FG"]
        stat_total["FGA"] += team_dict[i]["FGA"]
        stat_total["3P"] += team_dict[i]["3P"]
        stat_total["3PA"] += team_dict[i]["3PA"]
        stat_total["FT"]+=team_dict[i]["FT"]
        stat_total["FTA"]+=team_dict[i]["FTA"]
        stat_total["ORB"]+=team_dict[i]["ORB"]
        stat_total["DRB"]+=team_dict[i]["DRB"]
        stat_total["TRB"]+=team_dict[i]["TRB"]
        stat_total["AST"]+=team_dict[i]["AST"]
        stat_total["STL"]+=team_dict[i]["STL"]
        stat_total["BLK"]+=team_dict[i]["BLK"]
        stat_total["TOV"]+=team_dict[i]["TOV"]
        stat_total["PF"]+=team_dict[i]["PF"]
        stat_total["PTS"]+=team_dict[i]["PTS"]

    stat_total["FG%"] =round((stat_total["FG"]/stat_total["FGA"]),3)
    stat_total["3P%"] =round((stat_total["3P"]/stat_total["3PA"]),3)
    stat_total["FT%"] =round((stat_total["FT"]/stat_total["FTA"]),3)

    print(*stat_total.values(),sep="\t")

print("\n ********************************** \n")

print_nba_game_stats(team_dict["home_team"]["players_data"])
