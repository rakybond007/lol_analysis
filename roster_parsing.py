import numpy as np
import json
import csv

with open("./roster.json", "r", encoding='utf-8-sig') as f:
    data_roster = json.load(f)

data_parse = {}
seasons = data_roster.keys()
country = "Korea"
for season in seasons:
    teams = data_roster[season][country].keys()

    for team in teams:
        lines = data_roster[season][country][team].keys()
        data_parse[team+"_"+season] = {}
        for line in lines:
            players = data_roster[season][country][team][line].keys()
            
            for player in players:
                if data_roster[season][country][team][line][player] == "join":
                    data_parse[team+"_"+season][line] = 1
                else:
                    data_parse[team+"_"+season][line] = 0

# WRITE to CSV
print("WRITE CSV")
with open("./roster_result.csv", "w", encoding="utf-8", newline='') as f:
    wr = csv.writer(f)
    
    # column names
    data=['team_season']
    for s in ["Top", "Jungle", "Mid", "Bot", "Support", "Head_Coach"]:
        data.append(s)
    wr.writerow(data)

    # data
    team_seasons = data_parse.keys()
    for team_season in team_seasons:
        data = [team_season]
        for s in ["Top", "Jungle", "Mid", "Bot", "Support", "Head_Coach"]:
            data.append(data_parse[team_season][s])
        wr.writerow(data)