# Brady Madden

import csv

stats = {'2011': {}, '2012': {}, '2013': {}, '2014': {}, '2015': {}, '2016': {}}
tourn_skeleton = {'2011': [], '2012': [], '2013': [], '2014': [], '2015': [], '2016': []}
tourn_results = {'2011': [], '2012': [], '2013': [], '2014': [], '2015': [], '2016': []}


def organize_data():
    with open('data/ncaa_tournament_data.csv', 'r') as f:
        mainlist = iter(csv.reader(f))
        next(mainlist)
        for line in mainlist:
            year = int(line[1][:4]) + 1
            attr = []
            for l in line:
                attr.append(l)
            attr.pop(0)
            attr.pop(0)
            stats[str(year)][line[0]] = attr

    with open('data/tournament_datalists.txt') as t:
        for line in t:
            if line[0] == '[':
                line = line.replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace(", ",
                                                                                                         ",").split(",")
                tourn_results[str(year)] = line
            else:
                year = int(line[:4])

    for year in tourn_results.keys():
        temp_list = [None] * 127
        itr = 0
        while itr < 64:
            temp_list[itr] = tourn_results[year][itr]
            itr += 1
        tourn_skeleton[year] = temp_list


def bracket_comparator(year, trial):
    itr = 0
    misses = 0
    while itr < 127:
        if tourn_results[str(year)][itr] != trial[itr]:
            misses += 1
        itr += 1
    return misses


def compare_teams(year, t1, t2):
    t1_stats = stats[str(year)][str(t1)]
    t2_stats = stats[str(year)][str(t2)]
    if (int(t1_stats[0]) <= int(t2_stats[0])):
        return t1
    else:
        return t2


def build_bracket(year):
    bracket = tourn_skeleton[str(year)]
    i = 0
    while i < 126:
        t1 = bracket[i]
        t2 = bracket[i + 1]
        bracket[int(i / 2) + 64] = compare_teams(year, t1, t2)
        i += 2
    return bracket


def main():
    organize_data()
    # Number of errors based just on higher seed
    print(bracket_comparator(2011, build_bracket(2011)))


main()
