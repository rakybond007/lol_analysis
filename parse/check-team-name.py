


csv_teamnames = {}

for y in ['2018', '2019', '2020']:
    for s in ['spring', 'summer']:
        filename = "/home/user/lol_analysis/regular-season/"+y+"_"+s+".csv"

        print("==================================")
        print(y+"_"+s)

        teamnames = []
        with open(filename, "r") as f:
            lines = f.readlines()
            lines = lines[2:]

        for idx, line in enumerate(lines):
            teamname = line.split(",")[1][2:]
            pts = line.split(",")[-2]
            #print(teamname, "/", idx+1, "/", pts)
            teamnames.append([teamname, idx+1, pts])

        #sorted_teamnames = sorted(teamnames, lambda x: x[0])

        teamnames.sort(key = lambda x: x[0])
        for v in teamnames:
            print(v[0])

        with open("./check-team-name.txt", "a") as f:
            f.write("=====================================================================\n") 
            f.write(y+"_"+s+"\n")
            for a,b,c in teamnames:
                f.write(a+"\n")
                line = ',\n"Score": ' + '{\n\t'+'"rank":'+' "'+str(b)+'",\n'+'\t"pts": '+'"'+str(c)+'"'+'\n'+'}'+"\n"
                #print(a, "/", b, "/", c)
                f.write(line)
                #print(line)

        csv_teamnames[y+"_"+s] = teamnames
        #print(y+"_"+s, teamnames)

'''
import json
with open("/home/user/lol_analysis/roster.json", "r") as f:
    data = json.load(f)

json_teamnames = {}
keys = data.keys()
for key in keys:
    json_teamnames[key] = data[key]['Korea'].keys()
    #print(key, data[key]['Korea'].keys())


csv_years = ['2018', '2019', '2020']
csv_seasons = ['spring', 'summer']

json_years = ['2019', '2020', '2021']
json_seasons = ['Midseason', 'Preseason']

for x in csv_years:
    for y in csv_seasons:
        print(x+"_"+y)


for x in json_years:
    for y in json_seasons:
        print(x+"_"+y)


for c_y, j_y in zip(csv_years, json_years):
    for c_s, j_s in zip(csv_seasons, json_seasons):
        print('\n', c_y, c_s, j_y, j_s )
        print('csv', csv_teamnames[c_y+"_"+c_s])
        print('json', json_teamnames[j_y+"_"+j_s])
'''