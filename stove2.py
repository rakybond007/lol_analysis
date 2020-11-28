import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
pro_status_dict = {}
web_address = "https://lol.gamepedia.com/Roster_Swaps"
countries = ["Korea"]
seasons = ["Current", "2020_Midseason", "2020_Preseason", "2019_Midseason", "2019_Preseason", "2018_Midseason", "2018_Preseason"]
roster_dict = {}
progamer_set = set()
bar_down = 0

def crawl_roster():
    position_names = ["Top", "Jungle", "Mid", "Bot", "Support", "Head_Coach"]
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
                if i >= 10:
                    break
                table_info = table[i].select("tbody")[0].select("tr")
                if table[i].select("tbody")[0].select("tr.empty-width-row"):
                    roster_start_idx = 3
                    team_name_tr = table_info[1]
                else:
                    roster_start_idx = 2
                    team_name_tr = table_info[0]
                #team name no change
                print(season)
                if not team_name_tr.select("th.rosterswap-current-new"):
                    #print(team_name_tr.select("th")[1].find('a').attrs)
                    if not 'data-to-id' in team_name_tr.select("th")[1].find('a').attrs:
                        team_name = team_name_tr.select("th")[1].find('a').attrs['title']
                    else:
                        team_name = team_name_tr.select("th")[1].find('a').attrs['data-to-id']
                    #print(team_name)
                else:
                    team_name_prev_attrs = team_name_tr.select("th.rosterswap-current-old")[0].find('a').attrs
                    if not 'data-to-id' in team_name_prev_attrs:
                        team_name_prev = team_name_prev_attrs['title']
                    else:
                        team_name_prev = team_name_prev_attrs['data-to-id']
                    team_name_post_attrs = team_name_tr.select("th.rosterswap-current-new")[0].find('a').attrs
                    if not 'data-to-id' in team_name_prev_attrs:
                        team_name_post = team_name_post_attrs['title']
                    else:
                        team_name_post = team_name_post_attrs['data-to-id']
                    #team_name_post = team_name_tr.select("th.rosterswap-current-new")[0].find('a').attrs['data-to-id']
                    team_name = team_name_prev + ';' + team_name_post
                table_roster = table_info[roster_start_idx:]
                '''
                progamers_all_table = table[i].select("td.rosterswap-current-old")
                progamers_join_table = table[i].select("td.rosterswap-current-new.rosterswap-current-join")
                progamers_leave_table = table[i].select("td.rosterswap-current-old.rosterswap-current-leave")
                print(len(table[i].select("td.rosterswap-current-rolename")))
                '''
                rolenames = table[i].select("td.rosterswap-current-rolename")
                position_nums = []
                for role in rolenames:
                    position_nums.append(int(role.attrs['rowspan']))
                if not position_nums:
                    position_nums.append(int(table[i].select("tr.rosterswap-current-t.rosterswap-current-firstline")[0].select("td")[0].attrs['rowspan']))
                    #bbq 이상한거 처리
                    if team_name == "Bbq_Olivers" and season == "2018_Preseason":
                        position_nums[0] = 1
                    position_nums.append(int(table[i].select("tr.rosterswap-current-j.rosterswap-current-firstline")[0].select("td")[0].attrs['rowspan']))
                    position_nums.append(int(table[i].select("tr.rosterswap-current-m.rosterswap-current-firstline")[0].select("td")[0].attrs['rowspan']))
                    position_nums.append(int(table[i].select("tr.rosterswap-current-a.rosterswap-current-firstline")[0].select("td")[0].attrs['rowspan']))
                    position_nums.append(int(table[i].select("tr.rosterswap-current-s.rosterswap-current-firstline")[0].select("td")[0].attrs['rowspan']))
                #exit(1)
                #progamers_join_table = table[i].select("td.rosterswap-current-old.rosterswap-current-join")
                position_idx = 0
                line_per_num = 0
                roster_dict[season][country][team_name] = {}
                for each_player in table_roster:
                    if each_player.find('a') == None:
                        continue
                    progamer_id_attrs = each_player.find('a').attrs
                    if not 'data-to-id' in progamer_id_attrs:
                        progamer_id = progamer_id_attrs['title']
                    else:
                        progamer_id = progamer_id_attrs['data-to-id']
                    #progamer_id = each_player.find('a').attrs['data-to-id']
                    if len(progamer_id.split('_')) > 1:
                        progamer_id = progamer_id.split('_')[0]
                    progamer_set.add(progamer_id)
                    if line_per_num == position_nums[position_idx]:
                        position_idx += 1
                        line_per_num = 0
                    if line_per_num == 0:
                        roster_dict[season][country][team_name][position_names[position_idx]] = {}
                    # join 이 없는 라인. 떠나기만 했거나, 남아있거나.
                    if not each_player.select("td.rosterswap-current-new.rosterswap-current-join"):
                        # 떠난 사람
                        if each_player.select("td.rosterswap-current-old.rosterswap-current-leave"):
                            roster_dict[season][country][team_name][position_names[position_idx]][progamer_id] = "leave"
                        else:
                            roster_dict[season][country][team_name][position_names[position_idx]][progamer_id] = "origin"
                    # join 이 있는 라인. 전임자가 떠남.
                    else:
                        if each_player.select("td.rosterswap-current-old.rosterswap-current-leave"):
                            roster_dict[season][country][team_name][position_names[position_idx]][progamer_id] = "leave"
                            progamer_id_attrs_two = each_player.select('a')
                            join_gamer_attrs = progamer_id_attrs_two[1].attrs
                            if not 'data-to-id' in join_gamer_attrs:
                                join_progamer_id = join_gamer_attrs['title']
                            else:
                                join_progamer_id = join_gamer_attrs['data-to-id']
                            roster_dict[season][country][team_name][position_names[position_idx]][join_progamer_id] = "join"
                        else:
                            roster_dict[season][country][team_name][position_names[position_idx]][progamer_id] = "join"
                    line_per_num += 1

                # Past version code
                '''
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
                '''

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
            col_names[1] = "Games"
            print(col_names)
            exit(1)
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
'''
crawl_progamer_status("Chovy")
for pro in sorted(progamer_set):
    print(pro)
    crawl_progamer_status(pro)
with open('pro_status2.json', 'w', encoding='utf-8-sig') as pro_status_file:
    json.dump(pro_status_dict, pro_status_file, indent="\t", ensure_ascii=False)
'''
print(roster_dict)
with open('roster.json', 'w', encoding='utf-8') as roster_file:
    json.dump(roster_dict, roster_file, indent="\t")