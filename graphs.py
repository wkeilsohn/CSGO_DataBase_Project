# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 14:16:48 2019

@author: William Keilsohn
"""

'''
This file just makes graphs of the data.
All other data processing is handeled in other files.
'''

# Import packages:
import numpy as np
import pandas as pd
import seaborn as sns

# Import one of my own:
import questions as qu

### https://seaborn.pydata.org/tutorial/aesthetics.html
### https://seaborn.pydata.org/tutorial/color_palettes.html
### Produce uniform and asestetically pleasing plots:
sns.set_style('white')
sns.despine(offset = 10, trim = True)
sns.color_palette('hls', 8)

# Declare a variable for use later:
im_path = "C:/Users/kingw/Desktop/Data_Science_Project/py_graphs/"

# Define Line graphing functions:
def lineGrapher(df, num = 0): # https://seaborn.pydata.org/tutorial/regression.html#functions-to-draw-linear-regression-models
    cols = list(df)
    plt = sns.lmplot(x = cols[0], y = cols[1], data = df, x_estimator = np.mean)
    if num > 0:
        plt.savefig(im_path + 'fig' + str(num) + '.png') #https://stackoverflow.com/questions/32244753/how-to-save-a-seaborn-plot-into-a-file
    else:
        plt.savefig(im_path + "fig.png") 

    
# Define catigorical functions:
def boxGrapher(df, num = 0): # https://seaborn.pydata.org/tutorial/categorical.html#distributions-of-observations-within-categories
    cols = list(df)
    if len(cols) >= 3:
        if type(df.iloc[0,0]) == np.bool_:
            df = qu.dataStats.binaryChecker(df) # Just removing binary values.
        df1 = pd.DataFrame(df[cols[0]])
        df1.columns = ["Response"] # Ppt from last semester
        df1.insert(0, "Group", "First Treatment") # https://www.geeksforgeeks.org/python-pandas-dataframe-insert/
        df2 = pd.DataFrame(df[cols[1]])
        df2.columns = ["Response"]
        df2.insert(0, "Group", "Second Treatment") # https://www.geeksforgeeks.org/python-pandas-dataframe-insert/
        df = pd.concat([df1, df2]) #https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
        cols = list(df)
        del df1
        del df2 
    plt = sns.catplot(x = cols[0], y = cols[1], kind = 'box', data = df)
    if num > 0:
        plt.savefig(im_path + 'fig' + str(num) + '.png') #https://stackoverflow.com/questions/32244753/how-to-save-a-seaborn-plot-into-a-file
    else:
        plt.savefig(im_path + "fig.png")

    