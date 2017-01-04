# Brady Madden
# Scraping Sports-Reference.com to find NCAA Men's Basketball Tournament rankings for each team
import urllib.request
import csv
from bs4 import BeautifulSoup

years = [2016, 2015, 2014, 2013, 2012, 2011]

for year in years:
    # Write current tournment year in line before the teams/seeds
    with open('ncaa_tournament_data2.csv', 'a', newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([year])

    link = str("http://www.sports-reference.com/cbb/postseason/" + str(year) + "-ncaa.html")
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "html.parser")

    # Determine names of four regions
    brackets = soup.find('div', {'class': 'switcher filter'}).find_all('div')
    i = 0
    teams = []
    while i < 4:
        teams.append(brackets[i].a.string.lower())
        i += 1
    # Place each region's matchups into a seperate bracket variable
    bONE = soup.find('div', {'id': teams[0]}).div.div.find_all('div')
    bTWO = soup.find('div', {'id': teams[1]}).div.div.find_all('div')
    bTHREE = soup.find('div', {'id': teams[2]}).div.div.find_all('div')
    bFOUR = soup.find('div', {'id': teams[3]}).div.div.find_all('div')
    quad = [bONE, bTWO, bTHREE, bFOUR]
    # For each region loop through each matchup and record the team name and seed to CSV
    for region in quad:
        for matchup in region:
            t = matchup.find_all('div')
            for each in t:
                seed = each.span.string
                team = each.a['href'][13:][:-10].replace("-", " ").title()
                with open('ncaa_tournament_data2.csv', 'a', newline="") as f:
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow([str(team), seed])
    print(year, "done")
