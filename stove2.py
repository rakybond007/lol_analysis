import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
pro_status_dict = {}
web_address = "https://lol.gamepedia.com/Roster_Swaps"
countries = ["Korea"]
seasons = ["Current", "2020_Midseason", "2020_Preseason", "2019_Midseason", "2019_Preseason"]
roster_dict = {}
progamer_set = set()
bar_down = 0

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
                    progamer_set.add(progamer_id)
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
                    progamer_set.add(progamer_id)
                    roster_dict[season][country][team_name][progamer_id] = "join"

def crawl_progamer_status(pro_id):
    web_address = "https://lol.gamepedia.com/"
    seasons = ["2017", "2018", "2019", "2020"]
    pro_status_dict[pro_id] = {}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path='/home/hj/lol_analysis/chromedriver', chrome_options=chrome_options)
    for season in seasons:
        address = web_address + pro_id + "/Statistics/" +  season
        driver.get(address)
        source = requests.get(address).text
        table = driver.find_elements_by_class_name("wikitable")
        if not table:
            continue
        for season_idx in range(len(table)):
            table_heads = table[season_idx].find_element_by_tag_name("thead").find_elements_by_tag_name("tr")
            table_body = table[season_idx].find_element_by_tag_name("tbody")
            #get season name
            season_name_tag = table_heads[0].find_elements_by_tag_name("a")
            season_name = season_name_tag[1].get_attribute("title")
            pro_status_dict[pro_id][season_name] = {}

            #get table header infos
            Total_game_num = int(table_heads[1].find_element_by_tag_name("th").text.split(' ')[0])
            Total_champion_num = int(table_heads[1].find_element_by_tag_name("th").text.split(' ')[5])
            col_names_elements = table_heads[2].find_elements_by_tag_name("th")
            col_names = []
            for col_names_element in col_names_elements:
                col_names.append(col_names_element.text)
            
            #crawl table body
            body_elements_by_champion = table_body.find_elements_by_tag_name("tr")
            for champion_info in body_elements_by_champion:
                each_infos = champion_info.find_elements_by_tag_name("td")
                champion_name = each_infos[0].text
                pro_status_dict[pro_id][season_name][champion_name] = {}
                for info_idx in range(len(each_infos)):
                    pro_status_dict[pro_id][season_name][champion_name][col_names[info_idx]] = each_infos[info_idx].text
            #pro_status_dict[pro_id][season] = {}
    
#crawl_progamer_status("Canyon")
#exit(1)
crawl_roster()
print(sorted(progamer_set))
#crawl_progamer_status("Chovy")
for pro in sorted(progamer_set):
    print(pro)
    crawl_progamer_status(pro)
with open('pro_status2.json', 'w', encoding='utf-8-sig') as pro_status_file:
    json.dump(pro_status_dict, pro_status_file, indent="\t", ensure_ascii=False)
print(roster_dict)
with open('roster.json', 'w', encoding='utf-8') as roster_file:
    json.dump(roster_dict, roster_file, indent="\t")