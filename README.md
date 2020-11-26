# lol_analysis

##Selenium 쓰려면 크롬드라이버 받아야함. 네이버 검색해도 나오니 참고

###pro_status.json -> 각 프로게이머의 시즌별로 사용한 챔피언과 해당 챔피언의 평균 통계값 (킬, 어시, cs 등등) 을 map 형태로 만든 후 json dump한 파일
###roster.json -> 각 시즌별로, lck 의 각 팀 로스터 정보를 분석한 것. 남아있는 선수 : "origin" 떠난,떠나는 선수 : "leave", 새로 들어온 선수 : "join"
  *주의할점 : 감코도 포함되어 있는데, 코치는 없고 감독만 있음

####pro_status.json 구조 : pro_status_dict[선수id][시즌명][챔피언][각 정보 colname]
####roster.json 구조 : roster_dict[시즌명][리그국가][팀이름][선수id]
