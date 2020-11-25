import requests
from bs4 import BeautifulSoup

web_address = "https://lol.gamepedia.com/Roster_Swaps"
countries = ["Korea"]
seasons = ["Current"]

def crawl_stove():
    for season in seasons:
        for country in countries:
            address = web_address + "/" + season + "/" + country + "/Current_Rosters"
            source = requests.get(address).text
            soup = BeautifulSoup(source, "html.parser")
            table = soup.select("table.wikitable2.rosterswap-current")
            team_num = len(table)
            for i in range(team_num):
                progamers_all_table = table[i].select("td.rosterswap-current-old")
                progamers_leave_table = table[i].select("td.rosterswap-current-old.rosterswap-current-leave")
                progamers_new_table = table[i].select("td.rosterswap-current-old.rosterswap-current-join")
                print(len(progamers_all_table))
                print(progamers_all_table[0].find('a').attrs['data-to-id'])
                #print(progamers_all_table[0].select("a.data-to-id"))
                exit(1)
crawl_stove()