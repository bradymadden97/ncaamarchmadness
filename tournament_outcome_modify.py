# Brady Madden
# Modifies 'Outcome' column of ncaa_tournament_data.csv to make easier to read/ perform operations on
# In addition - format of 'Outcome' column in ncaa_tournament_data.csv changes from year to year
# Prior to 2016 tournament, First Four was called First Round, in 2016 tournament, Second Round was called First Round

import csv

newfile = open('ncaa_tournament_data_new.csv', 'a', newline="")
wr = csv.writer(newfile)
# Write headers
wr.writerow(['team_name', 'season', 'seed', 'wins', 'losses', 'sos', 'points_for', 'points_against',
             'AP_preseason', 'fg_pct', '3pt_pct', 'ft_pct', 'opp_fg_pct', 'opp_3pt_pct',
             'opp_ft_pct', 'O_reb', 'D_reb', 'opp_O_reb', 'opp_D_reb', 'turnover',
             'opp_turnover', 'ppg', 'opp_ppg', 'OUTCOME'])
with open('ncaa_tournament_data.csv', 'r') as f:
    # Skip headers when iterating over lines in CSV
    list = iter(csv.reader(f))
    next(list)
    # Iterate over each line
    for each in list:
        if each[1] != '2015-16':
            if each[-1] == 'Lost First Round':
                each[-1] = 'First_Four'
            elif each[-1] == 'Lost Second Round':
                each[-1] = 'Round_64'
            elif each[-1] == 'Lost Third Round':
                each[-1] = 'Round_32'
            elif each[-1] == 'Lost Regional Semifinal':
                each[-1] = 'Sweet_Sixteen'
            elif each[-1] == 'Lost Regional Final':
                each[-1] = 'Elite_Eight'
            elif each[-1] == 'Lost National Semifinal':
                each[-1] = 'Final_Four'
            elif each[-1] == 'Lost National Final':
                each[-1] = 'National_Final'
            elif each[-1] == 'Won National Final':
                each[-1] = 'Winner'
        elif each[1] == '2015-16':
            if each[-1] == 'Lost First Four':
                each[-1] = 'First_Four'
            elif each[-1] == 'Lost First Round':
                each[-1] = 'Round_64'
            elif each[-1] == 'Lost Second Round':
                each[-1] = 'Round_32'
            elif each[-1] == 'Lost Regional Semifinal':
                each[-1] = 'Sweet_Sixteen'
            elif each[-1] == 'Lost Regional Final':
                each[-1] = 'Elite_Eight'
            elif each[-1] == 'Lost National Semifinal':
                each[-1] = 'Final_Four'
            elif each[-1] == 'Lost National Final':
                each[-1] = 'National_Final'
            elif each[-1] == 'Won National Final':
                each[-1] = 'Winner'
        # Write to new file
        wr.writerow(each)
