# Brady Madden
# Scraping Sports-Reference.com for NCAA Men's Basketball information on Conference regular and postseason champion data

import csv
import urllib.request
from bs4 import BeautifulSoup

baselink = "http://www.sports-reference.com/cbb/conferences/"
page = urllib.request.urlopen(baselink)
soup = BeautifulSoup(page, "html.parser")

conferences = soup.find('table', {'id': 'active'}).find('tbody').find_all('tr')
links = []
for each in conferences:
    links.append("http://www.sports-reference.com" + str(each.find('td').a['href']))

# Traverse each conference page
for link in links:
    conference_name = link[48:].rstrip("/").replace('-', " ")
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "html.parser")
    years = soup.find('table', {'class': 'stats_table'}).find('tbody').find_all('tr')
    # Traverse each year from 2015-2016 back to 2010-2011 data
    for year in years:
        season = year.find('td', {'data-stat': 'season'}).string[:4]
        if season < '2010':
            break
        elif season != '2016':
            reg_season = year.find('td', {'data-stat': 'conf_champ'}).find_all('a')
            # If multiple regular season champions
            for each in reg_season:
                rchamp = each.get('href')[13:][:-10].replace("-", " ").title()
                filename = str(int(season) + 1) + "_regular_season_champions.csv"
                with open(filename, 'a', newline="") as f:
                    f.write(rchamp)
                    f.write("\n")
                print((str(int(season) + 1)), conference_name, "regular season done")
            # Scraping conference champions
            # If for Ivy league -> no conference championship
            if conference_name != 'ivy':
                # Try/except records missing records in a file for later manual upload
                try:
                    post_season = year.find('td', {'data-stat': 'conf_champ_post'}).find('a')
                    cchamp = post_season.get('href')[13:][:-10].replace("-", " ").title()
                    filename = str(int(season) + 1) + "_postseason_champions.csv"
                    with open(filename, 'a', newline="") as f:
                        f.write(cchamp)
                        f.write("\n")
                    print((str(int(season) + 1)), conference_name, "postseason done")
                except AttributeError:
                    filename = 'missing_conference_champs.csv'
                    with open(filename, 'a', newline="") as f:
                        f.write(str(int(season) + 1) + conference_name)
                        f.write('\n')
