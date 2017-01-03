# Brady Madden
# Parsing MasseyRatings.com for NCAA tournament data
# Must parse JSON files rather than scrape webpage due to dynamic webpage loading
import json
import urllib.request

base_link = "http://masseyratings.com/tournjson.php?t="
# Year parameters for 2011 - 2016 tournaments
year_refs = ['630', '639', '648', '660', '674', '689']
base_year = 2011
for y in year_refs:
    response = urllib.request.urlopen(base_link + y).read()
    json_data = json.loads(response.decode('utf-8'))['DI']

    tournament_data = [None] * 127
    c = 0
    counter = 0
    while counter < 68:
        seed = json_data[counter][1]
        team_name = json_data[counter][2][0]
        # Checking if eliminated in First Four
        if json_data[counter][8][1] != 'red':
            tournament_data[c] = team_name
            cur_index = c
            game_id = 9
            # Adding team to array for each win in tournament consistent with tree-ordering technique
            while game_id < 15 and json_data[counter][game_id][1] != 'red':
                cur_index = cur_index // 2 + 64
                tournament_data[cur_index] = team_name
                game_id += 1
            c += 1
        counter += 1
    file = open('data/tournament_datalists.txt', 'a', newline="")
    file.write(str(base_year) + ':\n')
    file.write(str(tournament_data))
    file.write('\n')
    print(str(base_year) + " tournament done")
    base_year += 1
