import csv
import re
def data_parser(filename):
    with open(filename, "r") as f:
        content = csv.reader(f, delimiter="|")
        body =[line for line in content]
    return body

def aggregrate(data_source):
    for each in data_source:
        try:
            data_source[each]["FG%"] =  round((data_source[each]["FG"]/data_source[each]["FGA"]),3)
        except:
            data_source[each]["FG%"] = 0.0
        try:
            data_source[each]["3P%"] =  round((data_source[each]["3P"]/data_source[each]["3PA"]), 3)
        except:
            data_source[each]["3P%"] = 0.0
        try:
            data_source[each]["FT%"] =  round((data_source[each]["FT"]/data_source[each]["FTA"]),3)
        except:
            data_source[each]["FT%"] = 0
        
        data_source[each]["TRB"] =  data_source[each]["ORB"] + data_source[each]["DRB"]
    return data_source

def add_player(play_data, action, action_name, add1=1):
    player_data ={"FG":0, "FGA":0, "FG%":0, "3P":0, "3PA":0, "3P%":0, "FT":0, "FTA":0, "FT%":0,
                	"ORB":0, "DRB":0, "TRB":0, "AST":0,	"STL":0, "BLK":0, "TOV":0, "PF":0, "PTS":0}
    try:
        if action in play_data.keys():
            play_data[action][action_name] +=add1
        else:
            play_data[action] = player_data
            play_data[action][action_name] = add1
    except:
        pass
    return play_data

def analyse_nba_game(play_by_play_moves):    
    home_data = dict()
    away_data = dict()
    noteam = dict()
    result = {"home_team": {"name": "", "players_data":home_data }, "away_team": {"name": "", "players_data": away_data}}
    i = 0
    for action in play_by_play_moves:
        cur_team = action[2]
        away_team = action[3]
        home_team = action[4]
        cur_action = action[-1]
        threepts = re.compile(r'(.*) makes 3-pt jump shot from').search(cur_action)
        threepts_miss = re.compile(r'(.*) misses 3-pt jump shot from').search(cur_action)
        turnover = re.compile(r'Turnover by (.*)\(').search(cur_action)
        rebound = re.compile(r'(.*) rebound by (.*)').search(cur_action)
        twopts = re.compile(r'(.*)makes 2-pt .*').search(cur_action)
        twopts_miss = re.compile(r'(.*)misses 2-pt .*').search(cur_action)
        freethrow = re.compile(r'(.*) makes free throw').search(cur_action)
        freethrow_path = re.compile(r'(.*) makes .* free throw').search(cur_action)
        freethrow_path_miss = re.compile(r'(.*) misses .* free throw').search(cur_action)
        freethrow_miss = re.compile(r'(.*) misses free throw').search(cur_action)
        pfoul = re.compile(r".* foul by (.*)").search(cur_action)
        if threepts:
            if cur_team == away_team:
                away_data  = add_player(away_data, threepts[1].strip(), "3P")
                away_data  = add_player(away_data, threepts[1].strip(), "3PA")
                away_data  = add_player(away_data, threepts[1].strip(), "PTS", 3)
                away_data  = add_player(away_data, threepts[1].strip(), "FG")
                away_data  = add_player(away_data, threepts[1].strip(), "FGA")
            else:
                home_data  = add_player(home_data, threepts[1].strip(), "3P")
                home_data  = add_player(home_data, threepts[1].strip(), "3PA")
                home_data  = add_player(home_data, threepts[1].strip(), "PTS", 3)
                home_data  = add_player(home_data, threepts[1].strip(), "FG")
                home_data  = add_player(home_data, threepts[1].strip(), "FGA")
            
            assists = re.compile(r'.* makes 3-pt .* \(assist by (.*)\)').search(cur_action)
            if assists:
                if cur_team != away_team:
                    home_data  = add_player(home_data, assists[1].strip(), "AST")
                else:
                    away_data  = add_player(away_data, assists[1].strip(), "AST")
        elif threepts_miss:
            if cur_team == away_team:
                away_data  = add_player(away_data, threepts_miss[1].strip(), "3PA")
                away_data  = add_player(away_data, threepts_miss[1].strip(), "FGA")
            else:
                home_data  = add_player(home_data, threepts_miss[1].strip(), "3PA")
                home_data  = add_player(home_data, threepts_miss[1].strip(), "FGA")
        elif turnover:
            if turnover[1].strip() == "Team":
                pass
            elif cur_team == away_team:
                away_data  = add_player(away_data, turnover[1].strip(), "TOV")
            else:
                home_data  = add_player(home_data, turnover[1].strip(), "TOV")
            steal = re.compile(r'Turnover by .*\(.*; steal by (.*)\)').search(cur_action)
            if steal:
                if cur_team == away_team:
                    home_data  = add_player(home_data, steal[1].strip(), "STL")
                else:
                    away_data  = add_player(away_data, steal[1].strip(), "STL")
        elif rebound:
            if rebound[2].strip() == "Team":
                pass
            else:
                code = "ORB" if rebound[1].strip() == "Offensive" else "DRB"
                if cur_team == away_team:
                    away_data  = add_player(away_data, rebound[2].strip(), code)
                else:
                    home_data  = add_player(home_data, rebound[2].strip(), code)
        elif twopts:
            if cur_team == away_team:
                away_data  = add_player(away_data, twopts[1].strip(), "PTS", 2)
                away_data  = add_player(away_data, twopts[1].strip(), "FG")
                away_data  = add_player(away_data, twopts[1].strip(), "FGA")
            else:
                home_data  = add_player(home_data, twopts[1].strip(), "PTS", 2)
                home_data  = add_player(home_data, twopts[1].strip(), "FG")
                home_data  = add_player(home_data, twopts[1].strip(), "FGA")
            assists = re.compile(r'.* makes 2-pt .* \(assist by (.*)\)').search(cur_action)
            if assists:
                if cur_team != away_team:
                    home_data  = add_player(home_data, assists[1].strip(), "AST")
                else:
                    away_data  = add_player(away_data, assists[1].strip(), "AST")
        elif twopts_miss:
            if cur_team == away_team:
                away_data  = add_player(away_data, twopts_miss[1].strip(), "FGA")
            else:
                home_data  = add_player(home_data, twopts_miss[1].strip(), "FGA")
            blocks = re.compile(r".* misses 2-pt .* \(block by (.*)\)").search(cur_action)
            if blocks:
                if cur_team != away_team:
                    away_data  = add_player(away_data, blocks[1].strip(), "BLK")
                else:
                    home_data  = add_player(home_data, blocks[1].strip(), "BLK")
        elif freethrow_path:
            if cur_team == away_team:
                away_data  = add_player(away_data, freethrow_path[1].strip(), "PTS")
                away_data  = add_player(away_data, freethrow_path[1].strip(), "FT")
                away_data  = add_player(away_data, freethrow_path[1].strip(), "FTA")
            else:
                home_data  = add_player(home_data, freethrow_path[1].strip(), "PTS",)
                home_data  = add_player(home_data, freethrow_path[1].strip(), "FT")
                home_data  = add_player(home_data, freethrow_path[1].strip(), "FTA")
        elif freethrow_path_miss:
            if cur_team == away_team:
                away_data  = add_player(away_data, freethrow_path_miss[1].strip(), "FTA")
            else:
                home_data  = add_player(home_data, freethrow_path_miss[1].strip(), "FTA")
        elif freethrow:
            if cur_team == away_team:
                away_data  = add_player(away_data, freethrow[1].strip(), "PTS")
                away_data  = add_player(away_data, freethrow[1].strip(), "FT")
                away_data  = add_player(away_data, freethrow[1].strip(), "FTA")
            else:
                home_data  = add_player(home_data, freethrow[1].strip(), "PTS",)
                home_data  = add_player(home_data, freethrow[1].strip(), "FT")
                home_data  = add_player(home_data, freethrow[1].strip(), "FTA")
        elif freethrow_miss:
            if cur_team == away_team:
                away_data  = add_player(away_data, freethrow_miss[1].strip(), "FTA")
            else:
                home_data  = add_player(home_data, freethrow_miss[1].strip(), "FTA")
        elif pfoul:
            if cur_action[-1] == ")":
                pfoul = re.compile(r".* foul by (.*) \(").search(cur_action)
            
            if pfoul[1].strip() in away_data.keys():
                away_data  = add_player(away_data, pfoul[1].strip(), "PF")
            elif pfoul[1].strip() in home_data.keys():
                home_data  = add_player(home_data, pfoul[1].strip(), "PF")
            else:
                try:
                    if pfoul[1].strip() in noteam.keys():
                        noteam[pfoul[1].strip()] += 1
                    else:
                        noteam[pfoul[1].strip()] = 1
                except:
                    noteam[pfoul[1].strip] = 1
    
    if noteam.keys():
        for each in noteam.keys():
            if each in away_data.keys():
                away_data = add_player(away_data, each, "PF", noteam[each])
            else:
                home_data = add_player(home_data, each, "PF", noteam[each])
    
    
    result["home_team"]["name"] = home_team
    result["home_team"]["players_data"] = aggregrate(home_data)
    result["away_team"]["name"] = away_team    
    result["away_team"]["players_data"] = aggregrate(away_data)
    return result

def print_nba_game_stats(team_dict):
    attr = ["FG",	"FGA",	"FG%", "3P", "3PA", "3P%","FT",	"FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV",	"PF",	"PTS"]
    print("Players\t", "FG\t",	"FGA\t",	"FG%\t", "3P\t", "3PA\t", "3P%\t","FT\t",	"FTA\t", "FT%\t", "ORB\t", "DRB\t", "TRB\t", "AST\t", "STL\t", "BLK\t", "TOV\t",	"PF\t",	"PTS")
    team_total = {"team":{}}
    for player in team_dict["players_data"].keys():
        print(player, end="\t\t")
        for each in attr:
            print(team_dict["players_data"][player][each],end="\t")
            try:
                team_total["team"][each] += team_dict["players_data"][player][each]
            except:
                team_total["team"][each] = 0
                team_total["team"][each] += team_dict["players_data"][player][each]
        print(end="\n")
    Team  = aggregrate(team_total)
    print("Team totals", end="\t")
    for each in attr:
        print(Team["team"][each], end="\t")
    
    print("",end="\n")

def my_test():
    play_by_play_moves = data_parser("nba_game_warriors_thunder_20181016.txt")#"new_db.txt")
    result = analyse_nba_game(play_by_play_moves)
    print_nba_game_stats(result["home_team"])

my_test()

mydict = {}

# mydict["name"] = {}
# mydict["name"]["price"] = 1
# mydict["name"]["goal"] = 1
# print(mydict)