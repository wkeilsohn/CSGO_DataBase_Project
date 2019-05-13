# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:50:16 2019

@author: William Keilsohn
"""

'''
This file cleans data to be inserted into the database.
It takes about 10hr to run.
Run with caution. 

I'm only providing the cleaned data, but all of it can be found here:
    https://www.kaggle.com/skihikingkevin/csgo-matchmaking-damage
'''

# Import packages:
import pandas as pd

# Specify file locations:
in_path = 'G:/'
out_path = 'E:/Cleaned_data/' # Had to go to the larger drive and then move it back.
heading = 'esea_master_'


# Obtain the data:
## https://stackoverflow.com/questions/25962114/how-to-read-a-6-gb-csv-file-with-pandas
ch_size = 50 # Don't want this to be too big...

# Define some needed constants.
teams = ['Team 1', 'Team 2', 'A', 'B', 'CounterTerrorist', 'Terrorist', 'Animal Style', 'Hentai Hooligans',]
bools = [True, False, True, False, True, False, True, False]
team_cols = ['att_team', 'vic_team', 'att_side', 'vic_side', 'winner_side', 'winner_team', 'bomb_site', 'is_bomb_planted']


# Write data cleaning function:
def boolChecker(df):
    for i in df.columns:
        if i in team_cols:
            # https://stackoverflow.com/questions/38001754/pandas-replace-column-values-to-empty-if-not-present-in-pre-defined-list
            df.loc[~df[i].isin(bools), i] = None
            df[i] = df[i].astype(bool)
        else:
            continue
    return df

def dataCleaner(data):
    # https://stackoverflow.com/questions/44988406/how-to-solve-error-due-to-chunksize-in-pandas
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
    data = data.replace(teams, bools)
    data = boolChecker(data)
    # https://www.postgresql.org/message-id/55D6639A.8040503%40aklaver.com
    data = data.where(pd.notnull(data), None)
    return data

# Deal with files:
def documentCleaner(inloc, outloc):
    df = pd.read_csv(inloc, chunksize = ch_size, iterator = True, skiprows = 0)
    # https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-fill
    with open(outloc, 'a') as j:
        for i in df:
            i = dataCleaner(i)
            i.to_csv(j, header = False)

# Note file locations:
ratios = pd.read_csv(out_path + 'ratio_data.csv', skiprows = 0)

# Handle all of the large data files:
fails = 0
for index, row in ratios.iterrows():
    if row[2] == 1:
        try:
            documentCleaner(in_path + heading + row[0], out_path + heading + row[1])
        except:
            fails += 1
            continue
    else:
        try:
            documentCleaner(in_path + row[0], out_path + row[1])
        except:
            fails += 1
            continue

# Checked that it worked:
if fails > 0:
    print('\n', 'A total of ' + str(fails) + ' documents failed to be converted.')
else:
    print('All documents converted sucessfully.')

        