# Brady Madden

import csv
import random
import numpy

seasons = [2011, 2012, 2013, 2014, 2015, 2016]
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


def build_bracket(year, score):
    bracket = tourn_skeleton[str(year)]
    i = 0
    while i < 126:
        t1 = bracket[i]
        t2 = bracket[i + 1]
        bracket[int(i / 2) + 64] = compare_teams(year, t1, t2, score)
        i += 2
    return bracket


def compare_teams(year, t1, t2, score):
    t1_stats = stats[str(year)][str(t1)]
    t2_stats = stats[str(year)][str(t2)]
    t1_pts = 0
    t2_pts = 0
    points = score

    res = compare_seed(t1_stats, t2_stats)
    if res == 'pull':
        t1_pts += float(points[0] / 2)
        t2_pts += float(points[0] / 2)
    elif res == 't1':
        t1_pts += float(points[0])
    else:
        t2_pts += float(points[0])

    res = compare_road_loss_pct(t1_stats, t2_stats)
    if res == 'pull':
        t1_pts += float(points[1] / 2)
        t2_pts += float(points[1] / 2)
    elif res == 't1':
        t1_pts += float(points[1])
    else:
        t2_pts += float(points[1])

    res = compare_sos(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[2])
    else:
        t2_pts += float(points[2])

    res = compare_spread(t1_stats, t2_stats)
    if res == 'pull':
        t1_pts += float(points[3] / 2)
        t2_pts += float(points[3] / 2)
    elif res == 't1':
        t1_pts += float(points[3])
    else:
        t2_pts += float(points[3])

    res = compare_ap_pre(t1_stats, t2_stats)
    if res == 'pull':
        t1_pts += float(points[4] / 2)
        t2_pts += float(points[4] / 2)
    elif res == 't1':
        t1_pts += float(points[4])
    else:
        t2_pts += float(points[4])

    res = compare_fg_pct(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[5])
    else:
        t2_pts += float(points[5])

    res = compare_3pt_pct(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[6])
    else:
        t2_pts += float(points[6])

    res = compare_ft_pct(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[7])
    else:
        t2_pts += float(points[7])

    res = compare_opp_fg_pct(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[8])
    else:
        t2_pts += float(points[8])

    res = compare_opp_3pt_pct(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[9])
    else:
        t2_pts += float(points[9])

    res = compare_oreb(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[10])
    else:
        t2_pts += float(points[10])

    res = compare_dreb(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[11])
    else:
        t2_pts += float(points[11])

    res = compare_opp_oreb(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[12])
    else:
        t2_pts += float(points[12])

    res = compare_opp_dreb(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[13])
    else:
        t2_pts += float(points[13])

    res = compare_turnover(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[14])
    else:
        t2_pts += float(points[14])

    res = compare_opp_turnover(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[15])
    else:
        t2_pts += float(points[15])

    res = compare_ppg(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[16])
    else:
        t2_pts += float(points[16])

    res = compare_opp_ppg(t1_stats, t2_stats)
    if res == 't1':
        t1_pts += float(points[17])
    else:
        t2_pts += float(points[17])

    res = was_rs_champ(t1_stats)
    res2 = was_rs_champ(t2_stats)
    if res is True and res2 is True or res is False and res2 is False:
        t1_pts += float(points[18] / 2)
        t2_pts += float(points[18] / 2)
    elif res is True:
        t1_pts += float(points[18])
    else:
        t2_pts += float(points[18])

    res = was_ps_champ(t1_stats)
    res2 = was_ps_champ(t2_stats)
    if res is True and res2 is True or res is False and res2 is False:
        t1_pts += float(points[19] / 2)
        t2_pts += float(points[19] / 2)
    elif res is True:
        t1_pts += float(points[19])
    else:
        t2_pts += float(points[19])

    if t1_pts > t2_pts:
        return t1
    elif t2_pts > t1_pts:
        return t2
    else:
        rand = [t1, t2]
        return random.shuffle(rand)[0]


def compare_seed(t1, t2):
    if (int(t1[0]) < int(t2[0])):
        return 't1'
    elif (int(t2[0]) < int(t1[0])):
        return 't2'
    else:
        return 'pull'


def compare_road_loss_pct(t1, t2):
    if abs(float(t1[3]) - float(t2[3])) <= 5:
        return 'pull'
    elif float(t1[3]) - float(t2[3]) > 5:
        return 't2'
    else:
        return 't1'


def compare_sos(t1, t2):
    if float(t1[4]) - float(t2[4]) > 0:
        return 't1'
    else:
        return 't2'


def compare_spread(t1, t2):
    s1 = float(t1[5]) - float(t1[6])
    s2 = float(t2[5]) - float(t2[6])
    if abs(s1 - s2) <= 1:
        return 'pull'
    elif s1 > s2:
        return 't1'
    else:
        return 't2'


def compare_ap_pre(t1, t2):
    if t1[7] and t2[7] is None:
        return 'pull'
    elif t1[7] is None:
        return 't2'
    elif t2[7] is None:
        return 't1'
    elif t1[7] < t2[7]:
        return 't1'
    else:
        return 't2'


def compare_fg_pct(t1, t2):
    if t1[8] < t2[8]:
        return 't1'
    else:
        return 't2'


def compare_3pt_pct(t1, t2):
    if t1[9] < t2[9]:
        return 't1'
    else:
        return 't2'


def compare_ft_pct(t1, t2):
    if t1[10] < t2[10]:
        return 't1'
    else:
        return 't2'


def compare_opp_fg_pct(t1, t2):
    if t1[11] < t2[11]:
        return 't1'
    else:
        return 't2'


def compare_opp_3pt_pct(t1, t2):
    if t1[12] < t2[12]:
        return 't1'
    else:
        return 't2'


def compare_oreb(t1, t2):
    if t1[14] < t2[14]:
        return 't1'
    else:
        return 't2'


def compare_dreb(t1, t2):
    if t1[15] < t2[15]:
        return 't1'
    else:
        return 't2'


def compare_opp_oreb(t1, t2):
    if t1[16] < t2[16]:
        return 't1'
    else:
        return 't2'


def compare_opp_dreb(t1, t2):
    if t1[17] < t2[17]:
        return 't1'
    else:
        return 't2'


def compare_turnover(t1, t2):
    if t1[18] < t2[18]:
        return 't1'
    else:
        return 't2'


def compare_opp_turnover(t1, t2):
    if t1[19] < t2[19]:
        return 't1'
    else:
        return 't2'


def compare_ppg(t1, t2):
    if t1[20] < t2[20]:
        return 't1'
    else:
        return 't2'


def compare_opp_ppg(t1, t2):
    if t1[21] < t2[21]:
        return 't1'
    else:
        return 't2'


def was_rs_champ(t):
    if t[22] == 1:
        return True
    else:
        return False


def was_ps_champ(t):
    if t[23] == 1:
        return True
    else:
        return False


def main():
    organize_data()
    prev_errors = None
    while prev_errors is None or prev_errors > 15:
        errors = 0
        scores = []
        for i in range(20):
            scores.append(random.random())
        for season in seasons:
            b = build_bracket(season, scores)
            errors += bracket_comparator(season, b)
        num_err = float(errors / 6)
        sort_idx = numpy.argsort(scores)
        print(num_err)
        with open('data/rand_score_sim_data.csv', 'a', newline="") as f:
            wr = csv.writer(f)
            wr.writerow([num_err, sort_idx, scores])
        if prev_errors is None or errors < prev_errors:
            prev_errors = errors


main()
