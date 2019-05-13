# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:54:01 2019

@author: William Keilsohn
"""

# Import Packages:


# Load additional relevant files:
# This was covered last semester but here is a run down:
# https://docs.python.org/2.0/ref/exec.html
stats_1 = 'C:/Users/kingw/Desktop/Data_Science_Project/stats_1.py'
graphs = 'C:/Users/kingw/Desktop/Data_Science_Project/graphs.py'
exec(open(stats_1).read())
#exec(open(graphs).read())

# Define sorting functions:
def normalFinder(df, bol = False):
    vals = dataShapiro(df, bol)
    re_val = 1
    for i in vals:
        if i < 0.5:
            re_val = 0
            break
    return re_val

def homogienFinder(df, bol = False):
    val = dataBartlett(df, bol)[1]
    if val < 0.5:
        re_val = 0
    else:
        re_val = 1
    return re_val

# Define logic: 
def cat_ord(df):
    val = normalFinder(df, True)
    if val == 1:
        val2 = homogienFinder(df, True)
        if val2 == 1:
            pv = dataANOVA(df)
        else:
            pv = dataKrusk(df)
    else:
        pv = dataKrusk(df)
    return pv

def ord_ord(df):
    val = normalFinder(df)
    if val == 1:
        pv = dataTtester(df)
    else:
        try:
            pv = dataWilcox(df)
        except:
            pv = dataTtester(df) # I know this isn't really acceptable statistically, but the way Wilcox is coded doesn't play nice with all dataframes.
    return pv