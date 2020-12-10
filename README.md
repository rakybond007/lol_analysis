# lol_analysis

## Crawling
### Execute
* Selenium 쓰려면 크롬드라이버 받아야함. 네이버 검색해도 나오니 참고
* 각 파이썬 파일을 python3 파일명 으로 실행하면 해당 파일명과 동일한 이름의 json 파일 만들어짐
* ` python3 stove.py ` or ` python3 stove2.py ` write roster.json   

### JSON files

* pro_status.json -> 각 프로게이머의 시즌별로 사용한 챔피언과 해당 챔피언의 평균 통계값 (킬, 어시, cs 등등) 을 map 형태로 작성
* pro_status_dict[선수id][시즌명][챔피언][각 정보 colname]
 
- roster.json -> 각 시즌별로, lck 의 각 팀 로스터 정보를 분석한 것. 남아있는 선수 : "origin" 떠난,떠나는 선수 : "leave", 새로 들어온 선수 : "join"
- 주의할점 : 감독/코치도 포함되어 있는데, 코치는 없고 감독만 있음
- roster_dict[시즌명][리그국가][팀이름][선수id]

* season_meta.json : season_meta_dict[시즌명] -> 순위순서대로 정렬된 리스트가 나옴. season_meta_dict[시즌명][0] : 해당 시즌의 1등 챔피언의 info dict
- team_score.json 구조 : team_score_dict[시즌명][팀이름][각 정보 colname]

## Parsing
* Execute py files in ./parse directory
- _parsing.py_ write 	&#42;-to-&#42;-avg.csv and 	&#42;-to-&#42;-ratio.csv files 
- It contains how much player's scores changed after stove-league. 
* _check-team-name.py_ match a player and the player's team
- _team-parsing.py_ write &#42;_Personal&Team_Score.csv 
- It contains score of players and team score which the player included

## Analysis
* team_analysis.R
* How much each liner changes affect to team score
- player_analysis.R
- How stove league affect to each players
* Personal&Team_Score.R
* How personal and team score affect to stove-league 
* And predict 2021 stove league results
