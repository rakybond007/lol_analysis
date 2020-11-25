import requests
from bs4 import BeautifulSoup
import json

web_address = "https://lol.gamepedia.com/Roster_Swaps"
countries = ["Korea"]
seasons = ["Current"]
roster_dict = {}

def crawl_roster():
    for season in seasons:
        for country in countries:
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
                team_name = table[i].find('th').find('a').attrs['data-to-id']
                if not team_name in roster_dict:
                    roster_dict[team_name] = {}
                for progamer in progamers_all_table:
                    if progamer.find('a') == None:
                        continue
                    progamer_id = progamer.find('a').attrs['data-to-id']
                    if len(progamer_id.split('_')) > 1:
                        progamer_id = progamer_id.split('_')[0]
                    roster_dict[team_name][progamer_id] = "origin"
                for progamer_leave in progamers_leave_table:
                    progamer_id = progamer_leave.find('a').attrs['data-to-id']
                    if len(progamer_id.split('_')) > 1:
                        progamer_id = progamer_id.split('_')[0]
                    roster_dict[team_name][progamer_id] = "leave"
                for progamer_join in progamers_join_table:
                    progamer_id = progamer_join.find('a').attrs['data-to-id']
                    if len(progamer_id.split('_')) > 1:
                        progamer_id = progamer_id.split('_')[0]
                    #print(progamer_id)
                    roster_dict[team_name][progamer_id] = "join"

crawl_roster()
print(roster_dict)
with open('roster.json', 'w', encoding='utf-8') as roster_file:
    json.dump(roster_dict, roster_file, indent="\t")