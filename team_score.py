import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
team_score_dict = {}
siteaddress1 = "http://lol.inven.co.kr/dataninfo/match/teamTotal.php?iskin=lol&category=&category2="
siteaddress2 = "&shipcode=&shipgroup="
seasons = ["LCK 2018 Spring", "LCK 2018 Spring PS", "LCK 2018 Summer", "LCK 2018 Summer PS", "LCK 2019 Spring", "LCK 2019 Spring PS", "LCK 2019 Summer", "LCK 2019 Summer PS", "LCK 2020 Spring", "LCK 2020 Spring PS", "LCK 2020 Summer", "LCK 2020 Summer PS", "Worlds 2018", "Worlds 2019", "Worlds 2020"]
seasons_code = ["112", "113", "116", "118", "20191", "126", "129", "131", "137", "138", "141", "142", "123", "135", "145"]
def crawl_team_status():
    for season_idx in range(len(seasons)):
        team_score_dict[seasons[season_idx]] = {}
        address = siteaddress1 + seasons_code[season_idx] + siteaddress2
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path='/home/hj/lol_analysis/chromedriver', chrome_options=chrome_options)
        driver.get(address)
        season_table = driver.find_element_by_class_name("listTable")
        # 헤더 정보 받아오기 -> column 이름
        col_names = season_table.find_element_by_tag_name("thead").find_element_by_tag_name("tr").find_elements_by_tag_name("th")
        # 바디
        team_infos = season_table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for info in team_infos:
            info_list = {}
            each_info = info.find_elements_by_tag_name("td")
            team_name = each_info[1].text
            for each_info_idx in range(len(each_info)):
                info_list[col_names[each_info_idx].text] = each_info[each_info_idx].text
            team_score_dict[seasons[season_idx]][team_name] = info_list
crawl_team_status()
print(team_score_dict)
with open('team_score.json', 'w', encoding='utf-8-sig') as team_score_file:
    json.dump(team_score_dict, team_score_file, indent="\t", ensure_ascii=False)