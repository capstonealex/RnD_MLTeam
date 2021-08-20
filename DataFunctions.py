from mainProcessing import RECORD_TIME
from mainProcessing import SAMPLE_RATE

import pandas as pd             # data processing, CSV file I/O (e.g. pd.read_csv)
import glob
import csv



ALLINTENTS = ["sitting","walking"]
def filenameIntent(filepath):
    for intent in ALLINTENTS:
        if (intent in filepath.lower()):
            return intent




ID_CURRSTATE = -2
SELECTROWS = [0, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, ID_CURRSTATE]      # time = 0, nonzero features are 29 -> 38 incl
STATIONARY_STATES = [4,2,5];



# <-> 2D List of csv rows
def getSelectRows(row):
    out = []
    for ind in SELECTROWS:
        out.append(row[SELECTROWS])
    return out



TRANSITIONS = ["sit>stand","stand>walk","stand>sit","walk>walk","walk>stand"]

# <-> Find Category
def categoriseIntent(prevState, nextState):
    state = ""
    
    # - From Sit
    if prevState == 5:
        state += "sit>"
        
        if nextState == 7:
            return(state + "stand")
        

    # - From Stand
    if prevState == 4:
        state += "stand>"
        # to Sit
        if nextState == 6:
            return(state + "sit")
        # to Walk
        if nextState == 8:
            return(state + "walk")
        

    # - From Walk: left or right foot
    if prevState == 2: # or prevState == right footforward
        state += "walk>"
        # to Stand
        if nextState == 11: # or nextState == right foot --> stand
            return(state + "stand")
        # to Walk
   
        
    # - We dun goofed, print what number next state was
    print("nextState N/A: " + state + "," + nextState)
    return( state +"NA")
   


# <-> Label the intent
def labelIntent(csvList, intentLabel, intent_ID):
    for listRow in csvList:
        listRow.append(intentLabel)
        listRow.append(intent_ID)
    return listRow



# <-> Cuts to filter Record time and  Sampling rate
def sampleIntent(csvList):
    # convert to samples and sample rate
    recordTime = RECORD_TIME*100;
    sampleRate = 100/SAMPLE_RATE;
    
    endRec = len(csvList)
    startRec = endRec - recordTime;
    
    filterList = []
    for rowList in range(startRec, endRec, sampleRate):
        filterList.append = rowList
    
    return filterList



# <-> Converts a list of strings to a string
def list2string(inlist):
    strlist = ""
    for cell in inlist:
        strlist += cell + ","
    strlist = strlist[:-1]
    return(strlist)



# <-> Converts a full csv to string form
def csvList2String(csvList):
    outString = ""
    for rowList in csvList:
        outString = list2string(rowList)
        outString = outString +"\n"
    return outString