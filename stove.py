import requests
from bs4 import BeautifulSoup
import json

web_address = "https://lol.gamepedia.com/Roster_Swaps"
countries = ["Korea"]
seasons = ["Current", "2020_Midseason", "2020_Preseason", "2019_Midseason", "2019_Preseason"]
roster_dict = {}

def crawl_roster():
    for season in seasons:
        if not season in roster_dict:
            roster_dict[season] = {}
        for country in countries:
            if not country in roster_dict[season]:
                roster_dict[season][country] = {}
            address = web_address + "/" + season + "/" + country + "/Current_Rosters"
            source = requests.get(address).text
            soup = BeautifulSoup(source, "html.parser")
            table = soup.select("table.wikitable2.rosterswap-current")
            team_num = len(table)
            for i in range(team_num):
                #print(roster_dict)
                progamers_all_table = table[i].select("td.rosterswap-current-old")
                progamers_join_table = table[i].select("td.rosterswap-current-new.rosterswap-current-join")
                progamers_leave_table = table[i].select("td.rosterswap-current-old.rosterswap-current-leave")
                #progamers_join_table = table[i].select("td.rosterswap-current-old.rosterswap-current-join")
                if table[i].find('th').find('a') == None:
                    team_name = progamers_all_table[0].find('a').attrs['data-to-id']
                else:
                    team_name = table[i].find('th').find('a').attrs['data-to-id']
                # 2020 mid season 설해원 같은 경우, 팀 로고 칸이 이상하게 구성되어 있고 선수 이름 있는 칸이랑 같은 종류의 태그에 팀이름 적혀있어서 처리
                if not team_name in roster_dict:
                    roster_dict[season][country][team_name] = {}
                for progamer in progamers_all_table:
                    if progamer.find('a') == None:
                        continue
                    if team_name == progamer.find('a').attrs['data-to-id']:
                        continue
                    progamer_id = progamer.find('a').attrs['data-to-id']
                    if len(progamer_id.split('_')) > 1:
                        progamer_id = progamer_id.split('_')[0]
                    roster_dict[season][country][team_name][progamer_id] = "origin"
                for progamer_leave in progamers_leave_table:
                    progamer_id = progamer_leave.find('a').attrs['data-to-id']
                    if len(progamer_id.split('_')) > 1:
                        progamer_id = progamer_id.split('_')[0]
                    roster_dict[season][country][team_name][progamer_id] = "leave"
                for progamer_join in progamers_join_table:
                    progamer_id = progamer_join.find('a').attrs['data-to-id']
                    if len(progamer_id.split('_')) > 1:
                        progamer_id = progamer_id.split('_')[0]
                    #print(progamer_id)
                    roster_dict[season][country][team_name][progamer_id] = "join"

crawl_roster()
print(roster_dict)
with open('roster.json', 'w', encoding='utf-8') as roster_file:
    json.dump(roster_dict, roster_file, indent="\t")