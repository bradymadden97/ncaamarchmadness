# Brady Madden
# Scraping Sports-Reference.com to find every NCAA Men's Basketball Tournament team
# since 2010-2011 and record their stats for that season, in addition to finish in NCAA Tournament
import urllib.request
import csv
from bs4 import BeautifulSoup

# To prevent accidentally overwriting of data in ncaa_tournament_data.csv
input("Press Enter to begin scraping")

# Write headings to CSV
with open('ncaa_tournament_data.csv', 'wt', newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(['team_name', 'season', 'wins', 'losses', 'sos', 'points_for', 'points_against',
                     'AP_preseason', 'fg_pct', '3pt_pct', 'ft_pct', 'opp_fg_pct', 'opp_3pt_pct',
                     'opp_ft_pct', 'O_reb', 'D_reb', 'opp_O_reb', 'opp_D_reb', 'turnover',
                     'opp_turnover', 'ppg', 'opp_ppg', 'OUTCOME'])

# Find each team in Sports-Reference's list of D-1 NCAA Men's Basketball Teams
olink = "http://www.sports-reference.com/cbb/schools/"
page = urllib.request.urlopen(olink)
soup = BeautifulSoup(page, "html.parser")
teamrows = soup.find('table', class_='stats_table').find('tbody').find_all('tr')
for each in teamrows:
    # Try/Except to ignore the mid-table heading rows that do not contain a team
    try:
        l = each.find('td', {"data-stat": 'school_name'}).find('a', href=True)
        # If team is currently active and has been to the NCAA Tournament, continue
        if each.find('td', {"data-stat": 'ncaa_count'}) != 0 and each.find('td',
                                                                           {"data-stat": 'year_max'}).string == str(
            2017):
            link = "http://www.sports-reference.com" + str(l['href'])
            teamname = link[44:].rstrip("/").replace("-", " ").title()
            pagetoo = urllib.request.urlopen(link)
            chickensoup = BeautifulSoup(pagetoo, "html.parser")
            stattable = chickensoup.find('table', class_='sortable stats_table')
            stattablebody = stattable.find('tbody')
            rows = stattablebody.find_all('tr')
            i = 0
            start = 2016
            while i < 10 and i < len(rows):
                if rows[i].find('td', {"data-stat": 'round_max'}).string is not None:
                    year = rows[i].find('td', {"data-stat": 'season'}).string
                    wins = rows[i].find('td', {"data-stat": 'wins'}).string
                    losses = rows[i].find('td', {"data-stat": 'losses'}).string
                    sos = rows[i].find('td', {"data-stat": 'sos'}).string
                    pts_for = rows[i].find('td', {"data-stat": 'pts_per_g'}).string
                    pts_against = rows[i].find('td', {"data-stat": 'opp_pts_per_g'}).string
                    ap_pre = rows[i].find('td', {"data-stat": 'rank_pre'}).string
                    tourn_outcome = rows[i].find('td', {"data-stat": 'round_max'}).string

                    newlink = link + str(start - i) + ".html"
                    # In case of broken link
                    try:
                        seasonpage = urllib.request.urlopen(newlink)
                        seasonsoup = BeautifulSoup(seasonpage, "html.parser")
                        seasontable = seasonsoup.find('table', {"id": "team_stats"})
                        seasonrows = seasontable.find_all('tr', class_='light_text')

                        fg_pct = seasonrows[0].find('td', {"data-stat": 'fg_pct'}).string.strip('st').strip('nd').strip(
                            'rd').strip('th')
                        three_pct = seasonrows[0].find('td', {"data-stat": 'fg3_pct'}).string.strip('st').strip(
                            'nd').strip(
                            'rd').strip('th')
                        ft_pct = seasonrows[0].find('td', {"data-stat": 'ft_pct'}).string.strip('st').strip('nd').strip(
                            'rd').strip('th')
                        oreb = seasonrows[0].find('td', {"data-stat": 'orb'}).string.strip('st').strip('nd').strip(
                            'rd').strip('th')
                        dreb = seasonrows[0].find('td', {"data-stat": 'drb'}).string.strip('st').strip('nd').strip(
                            'rd').strip('th')
                        turn = seasonrows[0].find('td', {"data-stat": 'tov'}).string.strip('st').strip('nd').strip(
                            'rd').strip('th')
                        ppg = seasonrows[0].find('td', {"data-stat": 'pts_per_g'}).string.strip('st').strip('nd').strip(
                            'rd').strip('th')

                        opp_fg_pct = seasonrows[1].find('td', {"data-stat": 'opp_fg_pct'}).string.strip('st').strip(
                            'nd').strip('rd').strip('th')
                        opp_three_pct = seasonrows[1].find('td', {"data-stat": 'opp_fg3_pct'}).string.strip('st').strip(
                            'nd').strip('rd').strip('th')
                        opp_ft_pct = seasonrows[1].find('td', {"data-stat": 'opp_ft_pct'}).string.strip('st').strip(
                            'nd').strip('rd').strip('th')
                        opp_oreb = seasonrows[1].find('td', {"data-stat": 'opp_orb'}).string.strip('st').strip(
                            'nd').strip(
                            'rd').strip('th')
                        opp_dreb = seasonrows[1].find('td', {"data-stat": 'opp_drb'}).string.strip('st').strip(
                            'nd').strip(
                            'rd').strip('th')
                        opp_turn = seasonrows[1].find('td', {"data-stat": 'opp_tov'}).string.strip('st').strip(
                            'nd').strip(
                            'rd').strip('th')
                        opp_ppg = seasonrows[1].find('td', {"data-stat": 'opp_pts_per_g'}).string.strip('st').strip(
                            'nd').strip('rd').strip('th')

                        # Write team data to CSV
                        with open('ncaa_tournament_data.csv', 'a', newline="") as f:
                            writer = csv.writer(f, delimiter=",")
                            writer.writerow([str(teamname), str(year), str(wins), str(losses), str(sos),
                                             str(pts_for), str(pts_against), str(ap_pre), str(fg_pct), str(three_pct),
                                             str(ft_pct), str(opp_fg_pct), str(opp_three_pct), str(opp_ft_pct),
                                             str(oreb),
                                             str(dreb), str(opp_oreb), str(opp_dreb), str(turn), str(opp_turn),
                                             str(ppg), str(opp_ppg), str(tourn_outcome)])
                        print(teamname, year, "done")
                    except urllib.error.HTTPError:
                        pass
                i += 1
    except AttributeError:
        pass
