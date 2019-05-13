# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 18:32:17 2019

@author: William Keilsohn
"""

'''
This file loads all the data into your databaase.
If you haven't already set up your tables, please run the builder file.
Additionally, this file uses cleaned data, so if you don't have the copies I provided, please run the cleaner file first.

That said, this does still take a while to run: approx. 7 hrs


Aslo, ingeneral, assume the following citation(s) for this file:
    https://www.postgresql.org/docs/9.1/sql-syntax.html
    http://initd.org/psycopg/
    https://www.udemy.com/the-complete-sql-bootcamp/learn/v4/content
'''


# Import Packages:
import psycopg2 as pg2
import pandas as pd
from datetime import datetime as dt

# Covered in class PPt on date/time conversion.
# I just want to time how long it takes to load the data. 
t1 = dt.now()


# Declare password:
pasW = '' # This was my password. Change it to whatever you set up.

# Declare path to files:
path = 'C:/Users/kingw/Desktop/Data_Science_Project/Cleaned_data/' # Using Windows b/c of SQL related reasons.
heading = 'esea_master_'

# Create Connection:
conn = pg2.connect(database = 'postgres', user = 'postgres', host = 'localhost', password = pasW)
### Just a note, this assumes you use the default database. if you don't, swap out the name.
cur = conn.cursor()

# Lots of data so we parse it out:
## https://stackoverflow.com/questions/25962114/how-to-read-a-6-gb-csv-file-with-pandas
ch_size = 20 # Data moves faster with a smaller chunk.

## https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
def dataLister(string, loc, num):
#    row_num = 0
    # https://towardsdatascience.com/why-and-how-to-use-pandas-with-large-data-9594dda2ea4c
    for i in pd.read_csv(loc, chunksize = ch_size, iterator = True):
        s_string = '(' + ((num -1) * ' %s,') + ' %s)'
        val_lst = []
        for index, row in i.iterrows():
            new_row = tuple(row)
            val_lst.append(new_row)
            ## https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
            var_string = ','.join(cur.mogrify(s_string, j ).decode('utf-8') for j in val_lst)
        cur.execute('INSERT INTO ' + string + ' VALUES '+ var_string) # These lines work, the following is just insurance.
        conn.commit() # Indentation matters.
    
ratios = pd.read_csv('C:/Users/kingw/Desktop/Data_Science_Project/ratio_data.csv', skiprows = 0)

fails = 0
for index, row in ratios.iterrows():
    if row[1] == 1:
        try:
            dataLister(row[0], path + heading + row[2], row[3])
        except:
            #print(row[0] + ' failed to fill')
            fails += 1
            continue
    else:
        try:
            dataLister(row[0], path + row[2], row[3])
        except:
            #print(row[0] + ' failed to fill')
            fails += 1
            continue

# Checked that it worked:
if fails > 0:
    print('\n', 'A total of ' + str(fails) + ' tables failed to load.')
else:
    print('All data loaded successfully!')

# Close the connection:
cur.close()

# Finish testing:
# Still from PPt.
end = dt.now()
duration = end - t1
print("It took a total of: ", duration, " for the data to be loaded into the database.")