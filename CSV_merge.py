#Brady Madden
#Merges each sorted seeding CSV into master ncaa_tournament_data.csv to add seeding data to teams

#Currently unfinished
import csv

with open('ncaa_tournament_data.csv', 'r') as f:
    data = [line for line in csv.reader(f)]
print(data)
