# Brady Madden
# Scrape the number of road losses for each team from Sports-Reference.com
# and compare to number of total losses to determine a road loss percentage

import csv
import urllib.request
from bs4 import BeautifulSoup

newfile = open('data/ncaa_tournament_data_new.csv', 'a', newline="")
wr = csv.writer(newfile)
# Write headers - including new headers
wr.writerow(['team_name', 'season', 'seed', 'wins', 'losses', 'road_loss_pct', 'sos', 'points_for', 'points_against',
             'AP_preseason', 'fg_pct', '3pt_pct', 'ft_pct', 'opp_fg_pct', 'opp_3pt_pct',
             'opp_ft_pct', 'O_reb', 'D_reb', 'opp_O_reb', 'opp_D_reb', 'turnover',
             'opp_turnover', 'ppg', 'opp_ppg', 'reg_season_champ', 'postseason_champ', 'OUTCOME'])

link = "http://www.sports-reference.com/cbb/schools/"
page = urllib.request.urlopen(link)
soup = BeautifulSoup(page, "html.parser")

with open('data/ncaa_tournament_data.csv', 'r') as f:
    # Skip header line in CSV
    mainlist = iter(csv.reader(f))
    next(mainlist)
    # Iterate over each line in master table
    for line in mainlist:
        teamname = line[0].replace(" ", "-").lower()
        year = str(int(line[1][:4]) + 1)
        losses = line[4]
        # Go to that team's year page
        indiv_link = link + teamname + '/' + year + '-schedule.html'
        indiv_page = urllib.request.urlopen(indiv_link)
        indiv_soup = BeautifulSoup(indiv_page, "html.parser")
        # Find schedule table and break down by rows
        rows = indiv_soup.find('table', {'id': 'schedule'}).find_all('tr')
        del rows[0]
        road_losses = 0
        # Iterate through each row (game) to find road losses
        for row in rows:
            try:
                loc = row.find('td', {'data-stat': 'game_location'}).string
                wl = row.find('td', {'data-stat': 'game_result'}).string
                if loc == '@' and wl == 'L':
                    road_losses += 1
            except AttributeError:
                break
        road_loss_pct = '%.2f'%((float(road_losses) / int(losses)) * 100)
        line.insert(5, road_loss_pct)
        with open('data/ncaa_tournament_data_new.csv', 'a', newline="") as z:
            wr.writerow(line)
        print(teamname, year, "done")