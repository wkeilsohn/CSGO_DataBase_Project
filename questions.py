# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:24:46 2019

@author: William Keilsohn
"""

'''
General overview of Python classes. Came in handy when 
trying to remember syntax. Please consider it a general citation:
    https://docs.python.org/3/tutorial/classes.html
'''

# Packages that must be imported:
import random
from datetime import datetime as dt

# Don't really need to re-import these when loaded in order, but...
import numpy as np
import pandas as pd

# https://docs.python.org/2.0/ref/exec.html
stats_2 = 'C:/Users/kingw/Desktop/Data_Science_Project/stats_2.py'
graphs = 'C:/Users/kingw/Desktop/Data_Science_Project/graphs.py'
exec(open(stats_2).read())
exec(open(graphs).read())


class dataSets:
    
    path1 = 'C:/Users/kingw/Desktop/Data_Science_Project/data_sets.txt'
    path2 = 'C:/Users/kingw/Desktop/Data_Science_Project/report_stats.txt'
    
    cols = ['Table', 'Rows', 'Special Commands', 'Test Number']
    
    def dataPreper(path = path1):
        file = open(path).read().split('\n') # https://stackoverflow.com/questions/14676265/how-to-read-a-text-file-into-a-list-or-an-array-with-python
        for i in range(len(file)):
            file[i] = file[i].split('--') # From ppt.
        return file
    
    file1 = dataPreper()
    file2 = dataPreper(path2)
    
    def dataFramer(set_Frame = file1, colz = cols):
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html
        return pd.DataFrame(set_Frame, columns = colz).fillna('').astype({'Test Number':'int64'})
        # Note: A typical game of CS:GO has at max 30 rounds. Thus, when relevant, many of the comparisons are restricted to <= 30 rounds.    
    
    def frameMaker(st1, st2, st3 = ''):
        try:
            data = dataCaller(st1, st2, st3)
            data = errorDropper(data)
        except:
            print("\nI'm sorry, but the commands you have entered are incorrect.")
            data = pd.DataFrame(np.random.randn(100).reshape(100,1)) # From PPt.
        return data
    
class dataStats:
    
    def testSelector(df, num):
        if num == 0:
            return ord_ord(df)
        elif num == 1:
            return cat_ord(df)
        elif num == 2:
            return dataChi(df)
        elif num == 3:
            data_str = 'Your correlation has a p-value of ' + str(dataCorrelator(df)) + ' and your regression model produced an R^2 and p-value of ' + str(dataRegressor(df))
            return data_str
        else:
            return 'Sorry, but that is not a valid option'
    
    def resultDisplay(df, answer):
        cols = list(df)
        res_str = 'Your comparison of ' + str(cols[1:]) + ' to ' + str(cols[0]) + ' produced a result of: ' + '\n' + str(answer)
        return res_str
    
    def binaryChecker(df):
        cols = list(df)
        if len(cols) == 3:
            df = df.replace({True: 1, False: 0}) # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
            df = pd.pivot_table(df, index = cols[2], aggfunc = sum)
        else:
            df = df 
        return df

class userQuestions:
    
    def __init__(self):
        self.intro = 'Would you like to enter your own search or run a pre-defined analyses? \n 1 - Enter your own \n 2 - Pre-defined \n 3 - Run Report Tests '
        self.table = 'Please enter a table name: '
        self.column = 'Please enter two comma seperated columns: '
        self.special = 'Please indicate a special comand, or simply press enter: '
        self.test = 'What kind of test would you like to perform? '
        self.gen = 'Enter a value: '
        self.fail_val = "\nI'm sorry, but that is not a viable option."
        self.contin = 'Would you like to continue? (Y/N): '
        self.note = 'This may take some time.'
        self.per_parse = 'Would you like to run all tests, or just a single test? \n 1 - All Tests (Takes some time) \n 2 - Single Test \n'
    
        self.pos_lis = ['Y', 'y', 'yes', 'Yes', 'YES', 'yEs', 'yES', 'YeS', 'yeS']
    
        self.test_dic = {0: 'T-test or Wilcoxon',
                         1: 'Anova or Kruskal',
                         2: 'Chi Square',
                         3: 'Correlation'}
    
    def startPrompt(self):
        try:
            print(self.intro)
            answer = int(input(self.gen))
            return answer
        except:
            print(self.fail_val)
            return 100
            
    def customPrompt(self):
        answers = []
        answers.append(input(self.table))
        answers.append(input(self.column))
        answers.append(input(self.special))
        return answers
    
    def testPrompt(self):
        print(self.test)
        print(self.test_dic)
        try:
            answer = int(input(self.gen))
            return answer
        except:
            print(self.fail_val)
            return 100
    
    def userContinue(self):
        in_val = input(self.contin)
        if in_val in self.pos_lis:
            return True
        else:
            return False
        
    def autoPathPicker(self):
        print(self.per_parse)
        try:
            answer = int(input(self.gen))
            return answer
        except:
            print(self.fail_val)
            return 100

class recorder:
    
    def __init__(self):
        self.path = 'C:/Users/kingw/Desktop/Data_Science_Project/stats_record.txt'
    
    def fileCreator(self): # Just initialize and clear out the file between runs.
        file = open(self.path, "w")
        file.write('File initiated at :' + str(dt.now()) + '\n') # From ppt on datetime.
        file.write("Statistical test results: \n")
        file.close()
        
    def fileWritter(self, line_str):
        file = open(self.path, "a")
        file.write(str(line_str) + '\n')
        file.close()
        
    def fileFinisher(self):
        file = open(self.path, "a")
        file.write('File finished at: ' + str(dt.now()) + '\n') # From ppt.
        file.close()       

class preparedStats:
    
    def rowSelector(df, num):
        try:
            return list(df.iloc[num, :])
        except:
            print('The row you have selected is not an option.')
            return 100
    
    def rowListTester(lst, save_val = 0):
        df = dataSets.frameMaker(lst[0], lst[1], lst[2])
        if type(df.iloc[0,0]) == bool:
            df = dataStats.binaryChecker(df)
        res_str = dataStats.resultDisplay(df, dataStats.testSelector(df, lst[3]))
        if lst[3] == 1:
            cor_tab = dataTukey(df)
        print(res_str, end = '\n')
        try:
            print(cor_tab)
        except:
            print()
        if save_val == 0:
            del df
            return res_str
        else:
            return df, res_str
    
    def allTester(df):
        print('\nThis is going to take quite a bit of time')
        print('\nOnly statistical tests will be run (no graphs)')
        rec = recorder()
        rec.fileCreator()
        for index, row in df.iterrows():
            try:
                res_str = preparedStats.rowListTester(row)
            except:
                res_str = 'Row number ' + str(index) + ' failed to perform.'
                print(res_str)
            rec.fileWritter(res_str)
        rec.fileFinisher()
                
    def rowTester(df):
        in_val = int(input('\nPlease enter a row number (Indexing starts at zero): '))
        try:
            row_val = df.iloc[in_val, :]
        except:
            print('\nThat is an invalid responce.')
            print('\nA row will now be selected for you.\n')
            in_val = random.randint(0, len(df)) # From Ppt
            row_val = df.iloc[in_val, :]
        df2 = preparedStats.rowListTester(row_val, 1)
        return df2, row_val[3]
        
class checkers:

    def testChecker(df, num):
        obj = userQuestions()
        while num != 100:
            try:
                res_val = dataStats.resultDisplay(df, dataStats.testSelector(df, num))
                if num == 1:
                    cor_tb = dataTukey(df)
                print(res_val, end = '\n')
                try:
                    print(cor_tb)
                except:
                    print()
                break
            except:
                print("The test you have selected does not match your data.\nPlease select a different test.\n")
                num = userQuestions.testPrompt(obj)
        return num




           