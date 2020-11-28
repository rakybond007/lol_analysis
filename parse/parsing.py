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

        total_WR = total_W / total_GAMES * 100



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
            '''
            if player == 'Bdd' and  ('2019' in season or '2020' in season):
                print(prev_WR, prev_GAMES, total_WR, total_GAMES)
            '''
        '''
        print('CHECK', player, season)
        if player == 'Bdd' and  ('2019' in season or '2020' in season):
            #print('VALUE', data_player[player][season])
            champions = data_player[player][season].keys()
            for c in champions:
                print(c)
                print('\t', data_player[player][season][c])

            print('PARSE', data_parse[player])
            input()
        '''
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


for prev in ['18', '19']:
    after = str(int(prev)+1); transfer = '20'+after+'_Preseason'

    filename = "./"+prev+"-to-"+after+"-ratio.csv"
    print("WRITE CSV AS ", filename)
    with open(filename, "w", encoding="utf-8", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['Player', 'Transfer', 'dt(KDA)', 'dt(WR)', 'dt(KPAR)'])

        players = data_parse.keys()
        for player in players:
            # no data for trasfer btw 2018 and 2019 OR no data in 2018   OR no data in 2019 
            if transfer not in data_transfer[player]:
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

            if after+"su_"+key in data and after +"sp_"+key in data:
                after_kda = ( data[after+"sp_"+key] * data[after+"sp_GAMES"] + data[after+"su_"+key] * data[after+"su_GAMES"] ) / (data[after+"sp_GAMES"] + data[after+"su_GAMES"]  )
            elif after+"su_"+key in data: 
                after_kda = data[after+"su_"+key]
            elif after+"sp_"+key in data:
                after_kda = data[after+"sp_"+key]

            delta_kda = after_kda - prev_kda

            # PARSE DELTA(WIN RATE)
            key = "WR"
            if prev+"su_"+key in data and prev +"sp_"+key in data:
                prev_WR = ( data[prev+"sp_"+key] * data[prev+"sp_GAMES"] + data[prev+"su_"+key] * data[prev+"su_GAMES"] ) / (data[prev+"sp_GAMES"] + data[prev+"su_GAMES"]  )
            elif prev+"su_"+key in data: 
                prev_WR = data[prev+"su_"+key]
            elif prev+"sp_"+key in data:
                prev_WR = data[prev+"sp_"+key]

            if after+"su_"+key in data and after +"sp_"+key in data:
                after_WR = ( data[after+"sp_"+key] * data[after+"sp_GAMES"] + data[after+"su_"+key] * data[after+"su_GAMES"] ) / (data[after+"sp_GAMES"] + data[after+"su_GAMES"]  )
            elif after+"su_"+key in data: 
                after_WR = data[after+"su_"+key]
            elif after+"sp_"+key in data:
                after_WR = data[after+"sp_"+key]

            delta_WR = after_WR - prev_WR
        
            # PARSE DELTA(KPAR)
            key = "KPAR"
            if prev+"su_"+key in data and prev +"sp_"+key in data:
                prev_KPAR = ( data[prev+"sp_"+key] * data[prev+"sp_GAMES"] + data[prev+"su_"+key] * data[prev+"su_GAMES"] ) / (data[prev+"sp_GAMES"] + data[prev+"su_GAMES"]  )
            elif prev+"su_"+key in data: 
                prev_KPAR = data[prev+"su_"+key]
            elif prev+"sp_"+key in data:
                prev_KPAR = data[prev+"sp_"+key]

            if after+"su_"+key in data and after +"sp_"+key in data:
                after_KPAR = ( data[after+"sp_"+key] * data[after+"sp_GAMES"] + data[after+"su_"+key] * data[after+"su_GAMES"] ) / (data[after+"sp_GAMES"] + data[after+"su_GAMES"]  )
            elif after+"su_"+key in data: 
                after_KPAR = data[after+"su_"+key]
            elif after+"sp_"+key in data:
                after_KPAR = data[after+"sp_"+key]

            delta_KPAR = after_KPAR - prev_KPAR

            # ['Player', 'Transfer', 'dt(KDA)', 'dt(WR)', 'dt(KPAR)']
            write_data = [player,  data_transfer[player][transfer], delta_kda, delta_WR, delta_KPAR]
            wr.writerow(write_data)




for prev in ['18', '19']:
    after = str(int(prev)+1); transfer = '20'+after+'_Preseason'

    filename = "./"+prev+"-to-"+after+"-avg.csv"
    print("WRITE CSV AS ", filename)
    with open(filename, "w", encoding="utf-8", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['Player', 'Transfer', 'dt(KDA)', 'dt(WR)', 'dt(KPAR)'])

        players = data_parse.keys()
        for player in players:
            # no data for trasfer btw 2018 and 2019 OR no data in 2018   OR no data in 2019 
            if transfer not in data_transfer[player]:
                continue
            elif ('18sp_KDA' not in data_parse[player] and '18su_KDA' not in data_parse[player]):
                continue
            elif ('19sp_KDA' not in data_parse[player] and '19su_KDA' not in data_parse[player]):    
                continue

            data = data_parse[player]

            # PARSE DELTA(KDA)
            key = "KDA"
            if prev+"su_"+key in data and prev +"sp_"+key in data:
                prev_kda = data[prev+"su_"+key] + data[prev+"sp_"+key]
            elif prev+"su_"+key in data: 
                prev_kda = data[prev+"su_"+key]
            elif prev+"sp_"+key in data:
                prev_kda = data[prev+"sp_"+key]

            if after+"su_"+key in data and after +"sp_"+key in data:
                after_kda = data[after+"su_"+key] + data[after+"sp_"+key]
            elif after+"su_"+key in data: 
                after_kda = data[after+"su_"+key]
            elif after+"sp_"+key in data:
                after_kda = data[after+"sp_"+key]

            delta_kda = after_kda - prev_kda

            # PARSE DELTA(WIN RATE)
            key = "WR"
            if prev+"su_"+key in data and prev +"sp_"+key in data:
                prev_WR =  data[prev+"su_"+key] + data[prev+"sp_"+key]
            elif prev+"su_"+key in data: 
                prev_WR = data[prev+"su_"+key]
            elif prev+"sp_"+key in data:
                prev_WR = data[prev+"sp_"+key]

            if after+"su_"+key in data and after +"sp_"+key in data:
                after_WR = data[after+"su_"+key] + data[after+"sp_"+key]
            elif after+"su_"+key in data: 
                after_WR = data[after+"su_"+key]
            elif after+"sp_"+key in data:
                after_WR = data[after+"sp_"+key]

            delta_WR = after_WR - prev_WR
        
            # PARSE DELTA(KPAR)
            key = "KPAR"
            if prev+"su_"+key in data and prev +"sp_"+key in data:
                prev_KPAR = ( data[prev+"sp_"+key] * data[prev+"sp_GAMES"] + data[prev+"su_"+key] * data[prev+"su_GAMES"] ) / (data[prev+"sp_GAMES"] + data[prev+"su_GAMES"]  )
            elif prev+"su_"+key in data: 
                prev_KPAR = data[prev+"su_"+key]
            elif prev+"sp_"+key in data:
                prev_KPAR = data[prev+"sp_"+key]

            if after+"su_"+key in data and after +"sp_"+key in data:
                after_KPAR = ( data[after+"sp_"+key] * data[after+"sp_GAMES"] + data[after+"su_"+key] * data[after+"su_GAMES"] ) / (data[after+"sp_GAMES"] + data[after+"su_GAMES"]  )
            elif after+"su_"+key in data: 
                after_KPAR = data[after+"su_"+key]
            elif after+"sp_"+key in data:
                after_KPAR = data[after+"sp_"+key]

            delta_KPAR = after_KPAR - prev_KPAR

            # ['Player', 'Transfer', 'dt(KDA)', 'dt(WR)', 'dt(KPAR)']
            write_data = [player,  data_transfer[player][transfer], delta_kda, delta_WR, delta_KPAR]
            wr.writerow(write_data)
