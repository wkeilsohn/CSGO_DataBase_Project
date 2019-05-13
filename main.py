# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 19:01:54 2019

@author: William Keilsohn
"""

# Please Run This File.

# Load additional relevant files:
# This was covered last semester but here is a run down:
# https://docs.python.org/2.0/ref/exec.html
stats_2 = 'C:/Users/kingw/Desktop/Data_Science_Project/stats_2.py'
graphs = 'C:/Users/kingw/Desktop/Data_Science_Project/graphs.py'
exec(open(stats_2).read())
exec(open(graphs).read())

# One File needs to be imported differently due to the nature of it's contents:
import questions as qu
import window as wd
ans = qu.userQuestions()

# Start Program:
print('\n Hello and welcome to CS;GO Data Analysist Tool')

# Create Logic Tree(?):
runChecker = True

while runChecker:
    print('\n')
    in_val = qu.userQuestions.startPrompt(ans)
    if in_val == 1: # This lets users ask their own questions.
        user_sql = qu.userQuestions.customPrompt(ans)
        data = qu.dataSets.frameMaker(user_sql[0], user_sql[1], user_sql[2])
        if len(data) == 100:
            continue
        else:
            data = qu.dataStats.binaryChecker(data)
            test_type = qu.userQuestions.testPrompt(ans)
            test_type = qu.checkers.testChecker(data, test_type)
            wd.graphLogic.askForGraph(data, test_type)
            del data
    elif in_val == 2: # These are all questions I could think to ask.
        tests = qu.dataSets.dataFramer() 
        option_val = qu.userQuestions.autoPathPicker(ans)
        if option_val == 100:
            continue
        elif option_val == 1:
            qu.preparedStats.allTester(tests)
        else:
            info = qu.preparedStats.rowTester(tests)
            wd.graphLogic.askForGraph(info[0][0], info[1])
            del info
    elif in_val == 3: # These are just the "interesting" ones.
        tests = qu.dataSets.dataFramer(qu.dataSets.file2)
        option_val = qu.userQuestions.autoPathPicker(ans)
        if option_val == 100:
            continue
        elif option_val == 1:
            qu.preparedStats.allTester(tests)
            wd.graphLogic.graphAsker(tests)
        else:
            info = qu.preparedStats.rowTester(tests)
            wd.graphLogic.askForGraph(info[0][0], info[1])
            del info
    else:
        continue
    runChecker = qu.userQuestions.userContinue(ans)
    
'''
Final Comments:
    - The last graph you made will print out at the very end. It is a result of seaborn.
    - Please install ALL packages. There is a good number of them, and they all get used.
    - If you want to run a demo, I would personally resomend options:
        -> 2 > 2 > 8 > y
'''
    