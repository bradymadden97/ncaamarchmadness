# Brady Madden
# Sort the CSV data in ncaa_tournament_data2.csv alphabetically by team, separated by tournament year

import csv
from operator import itemgetter

with open('ncaa_tournament_data2.csv', 'r') as f:
    data = [line for line in csv.reader(f)]
filename = ""
files = []
list = []
for line in data:
    if len(line) == 1:
        filename = str(line[0]) + '_seeding_sorted.csv'
        files.append(filename)
        list.append([])
    else:
        list[-1].append(line)
iterator = 0;
for each in list:
    each.sort(key=itemgetter(0))
    for e in each:
        with open(files[iterator], 'a', newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(e)
    print(files[iterator], "sorted")
    iterator += 1
