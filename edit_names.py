# Brady Madden
# Edit the team names in tournament_datalists.txt to match the team names in ncaa_tournament_data.csv

import csv

t1 = {'2011': [], '2012': [], '2013': [], '2014': [], '2015': [], '2016': []}
t2 = {'2011': [], '2012': [], '2013': [], '2014': [], '2015': [], '2016': []}

t3 = {'2011': [], '2012': [], '2013': [], '2014': [], '2015': [], '2016': []}
t4 = {'2011': [], '2012': [], '2013': [], '2014': [], '2015': [], '2016': []}


def find_non_match():
    with open('data/ncaa_tournament_data.csv', 'r') as f:
        mainlist = iter(csv.reader(f))
        next(mainlist)
        for line in mainlist:
            year = int(line[1][:4]) + 1
            t1[str(year)].append(line[0])
    with open('data/tournament_datalists.txt') as t:
        for line in t:
            if line[0] == '[':
                line = line.replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace(", ",
                                                                                                         ",").split(
                    ",")
                t2[str(year)] = line[:64]
            else:
                year = int(line[:4])
    for y in t1.keys():
        for each in t1[str(y)]:
            match = False
            for e in t2[str(y)]:
                if e == each:
                    match = True
            if match is False:
                t3[str(y)].append(each)
        for each in t2[str(y)]:
            match = False
            for e in t1[str(y)]:
                if e == each:
                    match = True
            if match is False:
                t4[str(y)].append(each)


def rewrite():
    filedata = None
    with open('data/tournament_datalists.txt', 'r') as g:
        filedata = g.read()
    yearlist = [2011, 2012, 2013, 2014, 2015, 2016]
    already_used = []
    for y in yearlist:
        for d in t3[str(y)]:
            print(d)
        if y not in already_used:
            for e in t4[str(y)]:
                x = input("Replace " + e + " with: ")
                filedata = filedata.replace(e, x)
            already_used.append(y)
    with open('data/tournament_datalists.txt', 'w') as h:
        h.write(filedata)


def main():
    find_non_match()
    rewrite()


main()
