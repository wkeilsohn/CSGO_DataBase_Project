# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 09:06:32 2019

@author: William Keilsohn
"""
'''
This file deals with cleaning up your computer after you're done with the project.
Major citation(s):
    https://www.postgresql.org/docs/9.1/sql-syntax.html
    http://initd.org/psycopg/
    https://www.udemy.com/the-complete-sql-bootcamp/learn/v4/content
'''
# Import Packages:
import psycopg2 as pg2
import pandas as pd

# Declare password:
pasW = '' # This was my password. Change it to whatever you set up.

# Create Connection:
conn = pg2.connect(database = 'postgres', user = 'postgres', password = pasW)
### Just a note, this assumes you use the default database. if you don't, swap out the name.
cur = conn.cursor()

# Create some of my own constants:
path = 'C:/Users/kingw/Desktop/Data_Science_Project/'
ratios = pd.read_csv(path + 'ratio_data.csv')

# Remove all tables and thus clean out your database:
try:
    rows = ''
    for index, row in ratios.iterrows():
        if row[0] in rows:
            continue
        else:
            rows = rows + row[0] + ', '
    rows = rows[:-2]
    cur.execute('DROP TABLE ' + rows + ';')
    print('All tables and data removed successfully.')
except:
    print('Your tables have already been cleared.')

# Close the database when complete:
cur.close()
conn.commit()
