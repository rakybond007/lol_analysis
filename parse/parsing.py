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
        if 'LCK' not in season and 'Promotion' in season:
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

            # print(player, season, champion, d)
            ## gpm += float(d['G/M']) * (W+L)
            kpar += float(d['KPAR'].replace("%","")) *(W+L) if "nan" not in d['KPAR'] else 0

            #gpms.append(float(d['G/M'])) # gold per miniute
            #kpars.append(float(d['KPAR'].replace("%",""))) # kill participant

        total_GAMES =  (total_L+total_W)

        total_D = total_D if total_D>0 else 1
        total_KDA = (total_K + total_A) / total_D

        ## total_GPM = gpm / total_GAMES #np.mean(gpms)
        total_KPAR = kpar / total_GAMES #np.mean(kpars)

        total_WR = total_L / total_GAMES * 100



        if 'Playoffs' not in season or (season.split(" ")[1][-2:]+season.split(" ")[-2][:2].lower()+"_KPAR") not in data_parse[player]:
            season_name = season.split(" ")[1][-2:]+season.split(" ")[-1][:2].lower()
            data_parse[player][season_name+"_KDA"] = total_KDA
            ## data_parse[player][season_name+"_G/M"] = total_GPM
            data_parse[player][season_name+"_KPAR"] = total_KPAR
            data_parse[player][season_name+"_WR"] = total_WR
            data_parse[player][season_name+"_K"] = total_K
            data_parse[player][season_name+"_D"] = total_D
            data_parse[player][season_name+"_A"] = total_A  
            data_parse[player][season_name+"_GAMES"] = total_L+total_W

        else:
            season_name = season.split(" ")[1][-2:]+season.split(" ")[-2][:2].lower()

            ## prev_GPM = data_parse[player][season_name+"_G/M"]
            prev_KPAR = data_parse[player][season_name+"_KPAR"]
            prev_WR = data_parse[player][season_name+"_WR"]

            prev_K = data_parse[player][season_name+"_K"]
            prev_D = data_parse[player][season_name+"_D"]
            prev_A = data_parse[player][season_name+"_A"]
            prev_GAMES = data_parse[player][season_name+"_GAMES"]

            
            data_parse[player][season_name+"_KDA"] = ((prev_K + total_K) + (prev_A + total_A)) / ((prev_D + total_D))
            ## data_parse[player][season_name+"_G/M"] = (prev_GPM*prev_GAMES + total_GPM*total_GAMES ) / (prev_GAMES + total_GAMES) 
            data_parse[player][season_name+"_KPAR"] = (prev_KPAR*prev_GAMES + total_KPAR*total_GAMES ) / (prev_GAMES + total_GAMES) 
            data_parse[player][season_name+"_WR"] = (prev_WR*prev_GAMES + total_WR*total_GAMES) / (prev_GAMES + total_GAMES)
            data_parse[player][season_name+"_K"] = total_K + prev_K
            data_parse[player][season_name+"_D"] = total_D + prev_D
            data_parse[player][season_name+"_A"] = total_A + prev_A
            data_parse[player][season_name+"_GAMES"] = prev_GAMES + total_GAMES


    
        print('CHECK', player, season)
        # print(data_parse[player])
        #print(data_parse)
        #input()

    if  data_parse[player]  == {}:
        data_parse.pop(player)



# Parsing Transfer
with open("../roster.json", "r", encoding='utf-8') as f:
    data_roster = json.load(f)
    data_roster['2021_Preseason'] = data_roster['Current'] 

data_transfer = {}

transfer_keys = []
#years = ['2018', '2019', '2020', '2021']
years = ['2019', '2020', '2021']
seasons = ['Preseason', 'Midseason']
for year in years:
    for season in seasons:
        if year == '2021' and season == 'Midseason':
            continue
        transfer_keys.append(year+"_"+season)


for key in transfer_keys:
    teams = data_roster[key]['Korea'].keys()
    for team in teams:
        players = data_roster[key]['Korea'][team].keys()
        for player in players:
            if player not in data_transfer:
                data_transfer[player] = {}
            
            value = data_roster[key]['Korea'][team][player]
            if value == 'origin':
                data_transfer[player][key] = 0
            else:
                data_transfer[player][key] = 1

print(data_transfer)




# WRITE to CSV
print("WRITE CSV")
with open("./player_result.csv", "w", encoding="utf-8", newline='') as f:
    wr = csv.writer(f)
    
    # column names
    data=['player']
    for s in ['18sp', '18su', '19sp', '19su', '20sp', '20su']:
        for g in ['KDA','KPAR', 'WR']:
            data.append(s+"_"+g)
    for key in transfer_keys:
        data.append(key)
    wr.writerow(data)

    # data
    players = data_parse.keys()
    for player in players:
        data = [player]
        for s in ['18sp', '18su', '19sp', '19su', '20sp', '20su']:
            for g in ['KDA', 'KPAR', 'WR']:
                if (s+"_"+g) in data_parse[player]:
                    data.append(data_parse[player][s+"_"+g])
                else:
                    data.append(' ')
        for key in transfer_keys:
            if key in data_transfer[player]:
                data.append(data_transfer[player][key])
            else:
                data.append(' ')
        wr.writerow(data)


with open("./18-to-19.csv", "w", encoding="utf-8", newline='') as f:

    