# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:33:39 2019

@author: William Keilsohn
"""

'''
This file is 1/X to handle data analysis.
As with the others relating to SQL, please assume the following citations for SQL related plugins:
     https://www.postgresql.org/docs/9.1/sql-syntax.html
     http://initd.org/psycopg/
     https://www.udemy.com/the-complete-sql-bootcamp/learn/v4/content
'''

# Import packages:
import numpy as np
import pandas as pd
import psycopg2 as pg2
from scipy.stats.stats import pearsonr
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.libqsturng import psturng
import warnings

# You know why this is here:
warnings.filterwarnings('ignore') # https://docs.python.org/2/library/warnings.html

# Declare password:
pasW = ''# This was my password. Change it to whatever you set up.

# Create Connection:
conn = pg2.connect(database = 'postgres', user = 'postgres', host = 'localhost', password = pasW)
### Just a note, this assumes you use the default database. if you don't, swap out the name.


# Begin tests:
'''
Just to note, any time large quantities of data are being called there is going to be some delay. 
This WILL pull it alot faster than from the file itself, but still please be aware of that.
'''

# Define a general call function:
def dataCaller(table, cols, cmd = ''):
    print('\nFetching data...')
    cur = conn.cursor()
    cur.execute('SELECT ' + cols + ' FROM ' + table + ' ' + cmd + ';')
    col_lst = cols.split(',')
    df = pd.DataFrame(cur.fetchall(), columns = col_lst).dropna() # Ppt
    cur.close()
    return df

# Define a function to clean any possilby errerous columns:
## Note, there are cases where it is not always worth running this.
def errorDropper(df): # https://stackoverflow.com/questions/24214941/python-pandas-dataframe-filter-negative-values
    df = df[(df.iloc[:,1:] >= 0).all(1)]
    return df

# Define a regression function:
def dataRegressor(df): # http://www.michaeljgrogan.com/statsmodels-sklearn-linear-regression/
    val_ls = stats.linregress(df.iloc[:,0], df.iloc[:,1])
    pv = val_ls[3]
    rv = val_ls[2] ** 2
    print('R-squared value is ', str(rv), end = '\n')
    print('p-value is ', str(pv))
    return rv, pv
    
    
# Define correlation functions:
def dataCorrelator(df): # https://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
    pv = pearsonr(df.iloc[:,0], df.iloc[:,1])[1]# Coordinates call just the p-value
    return pv

def dataChi(df): # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
    # https://stackoverflow.com/questions/39607540/count-the-number-of-occurrence-of-values-based-on-another-column?rq=1
    df2 = df.groupby(list(df)).size().reset_index(name = 'totals')
    pv = stats.chisquare(df2['totals'])
    del df2
    return pv
    
# Define T-test functions:
def dataTtester(df): #https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.ttest_ind.html
    cols = list(df)
    if len(cols) == 3:
        df1 = pd.pivot_table(df, values = cols[0], index = cols[2], aggfunc = sum) # Ppt
        df2 = pd.pivot_table(df, values = cols[1], index = cols[2], aggfunc = sum)
        df = pd.concat([df1, df2], axis = 1) # https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
    pv = stats.ttest_ind(df.iloc[:,0], df.iloc[:,1])
    return pv

def dataWilcox(df):# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.wilcoxon.html
    cols = list(df)
    if len(cols) == 3:
        df1 = pd.pivot_table(df, values = cols[0], index = cols[2], aggfunc = sum) # Ppt
        df2 = pd.pivot_table(df, values = cols[1], index = cols[2], aggfunc = sum)
        df = pd.concat([df1, df2], axis = 1) #https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
    df.insert(0, "Difference", df.iloc[:, 0] - df.iloc[:, 1]) # https://www.geeksforgeeks.org/python-pandas-dataframe-insert/
    pv = stats.wilcoxon(df.iloc[:,0])
    return pv

# Define ANOVA functions:
def dataANOVA(df): # https://www.marsja.se/four-ways-to-conduct-one-way-anovas-using-python/
    if len(list(df)) > 2:
        pv = stats.f_oneway(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2])
    else:
         df = catSort(df)
         pv = getattr(stats, 'f_oneway')(*df) # https://stackoverflow.com/questions/11881700/call-function-with-a-dynamic-list-of-arguments-in-python
    return pv

def dataKrusk(df): # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html
    if len(list(df)) > 2:
        pv = stats.kruskal(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2])
    else:
         df = catSort(df)
         pv = getattr(stats, 'f_oneway')(*df) # https://stackoverflow.com/questions/11881700/call-function-with-a-dynamic-list-of-arguments-in-python
    return pv

# Assumptions:
def catSort(df):
    vals = []
    col1, col2 = list(df)[0], list(df)[1]
    for i in df[col1].unique(): # https://stackoverflow.com/questions/27241253/print-the-unique-values-in-every-column-in-a-pandas-dataframe
        # https://stackoverflow.com/questions/36684013/extract-column-value-based-on-another-column-pandas-dataframe
        vals.append(list(df.loc[df[col1] == i, col2]))
    return vals
       
def dataBartlett(df, bol = False): # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.bartlett.html       
    if bol:
      df = catSort(df)
      pv = getattr(stats, 'bartlett')(*df) # https://stackoverflow.com/questions/11881700/call-function-with-a-dynamic-list-of-arguments-in-python
    else:
      if len(list(df)) > 2:
          pv = stats.bartlett(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2])
      else:
          pv = stats.bartlett(df.iloc[:,0], df.iloc[:,1])
    return pv
    
def dataShapiro(df, bol = False): # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
    p_vals = []
    if bol:
        df = catSort(df)
        for i in df:
            p_vals.append(stats.shapiro(i)[1])
    else:
        for i in list(df):
            p_vals.append(stats.shapiro(df[i])[1])
    return p_vals

# Post Hoc Test:
def dataTukey(df): # https://stackoverflow.com/questions/16049552/what-statistics-module-for-python-supports-one-way-anova-with-post-hoc-tests-tu
    t_table = pairwise_tukeyhsd(df.iloc[:,1], df.iloc[:,0])
    p_vals = psturng(np.abs(t_table.meandiffs / t_table.std_pairs), len(t_table.groupsunique), t_table.df_total)
    # https://stackoverflow.com/questions/40516810/saving-statmodels-tukey-hsd-into-a-python-panda-dataframe
    t_frame = pd.DataFrame(data = t_table._results_table.data[1:], columns = t_table._results_table.data[0])
    t_frame.insert(5, "P-values", p_vals) # https://www.geeksforgeeks.org/python-pandas-dataframe-insert/
    return t_frame