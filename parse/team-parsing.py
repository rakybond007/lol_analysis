import numpy as np
import json
import csv

with open("../pro_status2.json", "r", encoding='utf-8-sig') as f:
    data_player = json.load(f)

data_parse = {}
players = data_player.keys()
for player in players:
    seasons = data_player[player].keys()

    data_parse[player] = {}
    for season in seasons:
        if 'LCK' not in season or 'Promotion' in season:
            continue
        elif 'Spring' not in season and 'Summer' not in season:
            continue

        if player == "Doran":
            print(player, season)

        champions = data_player[player][season].keys()
        total_K = 0; total_D = 0; total_A = 0; total_W =0; total_L=0
        gpms = []; kpars = []; gpm =0; kpar= 0 
        for champion in champions:
            d = data_player[player][season][champion]
            

            num_game = float(d['W']) + float(d['L'])
            K = float(d['K']) * num_game
            D = float(d['D']) * num_game
            A = float(d['A']) * num_game
            total_K += K; total_D += D; total_A += A
            
            W = float( d['W'])
            L = float( d['L'])
            total_W += W; total_L += L

            kpar += float(d['KPAR'].replace("%","")) *(W+L) if "nan" not in d['KPAR'] else 0

        total_GAMES =  (total_L+total_W)

        total_D = total_D if total_D>0 else 1
        total_KDA = (total_K + total_A) / total_D

        total_KPAR = kpar / total_GAMES 

        total_WR = total_W / total_GAMES * 100



        if 'Playoffs' not in season or (season.split(" ")[1][-2:]+season.split(" ")[-2][:2].lower()+"_KPAR") not in data_parse[player]:
            season_name = season.split(" ")[1][-2:]+season.split(" ")[-1][:2].lower() # ex 18sp / 18su
            data_parse[player][season_name+"_KDA"] = total_KDA
            data_parse[player][season_name+"_KPAR"] = total_KPAR
            data_parse[player][season_name+"_WR"] = total_WR
            data_parse[player][season_name+"_K"] = total_K
            data_parse[player][season_name+"_D"] = total_D
            data_parse[player][season_name+"_A"] = total_A  
            data_parse[player][season_name+"_GAMES"] = total_L+total_W

        else:
            season_name = season.split(" ")[1][-2:]+season.split(" ")[-2][:2].lower()

            prev_KPAR = data_parse[player][season_name+"_KPAR"]
            prev_WR = data_parse[player][season_name+"_WR"]

            prev_K = data_parse[player][season_name+"_K"]
            prev_D = data_parse[player][season_name+"_D"]
            prev_A = data_parse[player][season_name+"_A"]
            prev_GAMES = data_parse[player][season_name+"_GAMES"]

            
            data_parse[player][season_name+"_KDA"] = ((prev_K + total_K) + (prev_A + total_A)) / ((prev_D + total_D))
            data_parse[player][season_name+"_KPAR"] = (prev_KPAR*prev_GAMES + total_KPAR*total_GAMES ) / (prev_GAMES + total_GAMES) 
            data_parse[player][season_name+"_WR"] = (prev_WR*prev_GAMES + total_WR*total_GAMES) / (prev_GAMES + total_GAMES)
            data_parse[player][season_name+"_K"] = total_K + prev_K
            data_parse[player][season_name+"_D"] = total_D + prev_D
            data_parse[player][season_name+"_A"] = total_A + prev_A
            data_parse[player][season_name+"_GAMES"] = prev_GAMES + total_GAMES


    if  data_parse[player]  == {}:
        data_parse.pop(player)



# Parsing Transfer
with open("../roster.json", "r", encoding='utf-8') as f:
    data_roster = json.load(f)
    data_roster['2021_Preseason'] = data_roster['Current'] 

# data_roster['Chovy']['2019_Preseason']= [0, 'Griffin']
data_transfer = {}

transfer_keys = []
years = ['2019', '2020', '2021']
roster_seasons = ['Preseason', 'Midseason']
for year in years:
    for season in roster_seasons:
        if year == '2021' and season == 'Midseason':
            continue
        transfer_keys.append(year+"_"+season)


for key in transfer_keys:
    print('SEASON', key)
    teams = data_roster[key]['Korea'].keys()
    for team in teams:
        positions = data_roster[key]['Korea'][team].keys()
        for position in positions:
            players = data_roster[key]['Korea'][team][position].keys()
            for player in players:
                if player not in data_transfer:
                    data_transfer[player] = {}
                
                #print(team)
                teamname = team.split(",")[-1]
                if 'Score' not in data_roster[key]['Korea'][team]:
                    print("NO DATA", teamname, 'in', key)
                else:    
                    teamrank = data_roster[key]['Korea'][team]['Score']['rank']
                    teampts = data_roster[key]['Korea'][team]['Score']['pts']

                value = data_roster[key]['Korea'][team][position][player]
                if value == 'origin':
                    leave_or_not = 0
                else:
                    leave_or_not = 1

                if player == 'Edge':   
                    print(player,'\t', teamname,'\t', key)
                    print(data_transfer[player])
                data_transfer[player][key] = [leave_or_not, teamname, teamrank, teampts]
            
        
#print(data_transfer)


'''
# PARSE TEAM SCORE
team_scores = {}
for y in ['2018', '2019', '2020']:
    for s in ['spring', 'summer']:
        team_scores[y+"_"+s] = {}
        filename = "../regular-season/"+y+"_"+s+".csv"
        with open(filename, "r") as f:
            lines = f.readlines()
            lines = lines[2:]
            
        for idx, line in enumerate(lines):
            teamname = line.split(",")[1][2:]
            rank = line.split(",")[0]
            pts = line.strip().split(",")[-2]
            team_scores[y+"_"+s][teamname]={'rank': rank, 'pts':pts}


'''
# WRITE SCORE
for prev in ['18', '19']:
    after = str(int(prev)+1); transfer = '20'+after+'_Preseason'

    filename = "./"+prev+"_Personal&Team_Score.csv"
    print("WRITE CSV AS ", filename)
    with open(filename, "w", encoding="utf-8", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['Player', 'Transfer', 'KDA', 'WR', 'KPAR', 'Team-Rank', 'Team-Pts'])

        players = data_parse.keys()
        for player in players:
            # no data for trasfer btw 2018 and 2019    OR no data in 2018   OR no data in 2019 
            if player not in data_transfer:
                continue # for Edge (just in 2018 preseason)
            elif transfer not in data_transfer[player]:
                continue
            elif ('18sp_KDA' not in data_parse[player] and '18su_KDA' not in data_parse[player]):
                continue
            elif ('19sp_KDA' not in data_parse[player] and '19su_KDA' not in data_parse[player]):    
                continue

            data = data_parse[player]

            # PARSE DELTA(KDA)
            key = "KDA"
            if prev+"su_"+key in data and prev +"sp_"+key in data:
                prev_kda = ( data[prev+"sp_"+key] * data[prev+"sp_GAMES"] + data[prev+"su_"+key] * data[prev+"su_GAMES"] ) / (data[prev+"sp_GAMES"] + data[prev+"su_GAMES"]  )
            elif prev+"su_"+key in data: 
                prev_kda = data[prev+"su_"+key]
            elif prev+"sp_"+key in data:
                prev_kda = data[prev+"sp_"+key]

            # PARSE DELTA(WIN RATE)
            key = "WR"
            if prev+"su_"+key in data and prev +"sp_"+key in data:
                prev_WR = ( data[prev+"sp_"+key] * data[prev+"sp_GAMES"] + data[prev+"su_"+key] * data[prev+"su_GAMES"] ) / (data[prev+"sp_GAMES"] + data[prev+"su_GAMES"]  )
            elif prev+"su_"+key in data: 
                prev_WR = data[prev+"su_"+key]
            elif prev+"sp_"+key in data:
                prev_WR = data[prev+"sp_"+key]

            # PARSE DELTA(KPAR)
            key = "KPAR"
            if prev+"su_"+key in data and prev +"sp_"+key in data:
                prev_KPAR = ( data[prev+"sp_"+key] * data[prev+"sp_GAMES"] + data[prev+"su_"+key] * data[prev+"su_GAMES"] ) / (data[prev+"sp_GAMES"] + data[prev+"su_GAMES"]  )
            elif prev+"su_"+key in data: 
                prev_KPAR = data[prev+"su_"+key]
            elif prev+"sp_"+key in data:
                prev_KPAR = data[prev+"sp_"+key]


            # wr.writerow(['Player', 'Transfer', 'KDA', 'WR', 'KPAR', 'Team-Rank', 'Team-Pts'])
            #teamname = data_roster[player]['20'+prev+"_"] # data_roster['Chovy']['2019_Preseason']= [0, 'Griffin', 1, 16]
            write_data = [player, data_transfer[player][transfer][0], prev_kda, prev_WR, prev_KPAR, data_transfer[player][transfer][-2], data_transfer[player][transfer][-1]]
            wr.writerow(write_data)
